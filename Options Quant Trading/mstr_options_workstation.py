from __future__ import annotations

from datetime import date, datetime, timedelta
import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers the '3d' projection
from scipy.stats import lognorm

from databento_options import (
    DatabentoConfig,
    enrich_chain_with_quotes,
    estimate_request_cost,
    fetch_cmbp1_snapshot,
    fetch_option_definitions,
    sample_mstr_chain,
)
from mstr_options_lab.greeks import trader_unit_scales
from mstr_options_lab.implied_dist import (
    compute_implied_distribution,
    ImpliedDistribution,
    heston_pdf_for_expiry,
    slice_to_otm_smile,
)
from mstr_options_lab.pricing import calibrate_heston, CalibrationResult
from mstr_options_lab.pricing.black_scholes import bs_implied_vol, bs_price
from mstr_options_lab.pricing.carr_madan import fft_prices_many_strikes
from mstr_options_lab.pricing.characteristic_fns import heston_cf
from mstr_options_lab.surface.svi import svi_iv
from mstr_options_lab.data.ibkr import IBKRClient, IBKRConfig, IB_INSYNC_AVAILABLE
from mstr_options_lab.data.databento_live import DatabentoLiveClient
from mstr_options_lab.greeks.chain import compute_chain_greeks


# Source order: Sample (offline dev), Databento Hist (research), IBKR (full IB),
# Hybrid Live = recommended (IB spot + Databento OPRA chain — uses each source
# for what it's actually best at).
DATA_SOURCES = ["Sample", "Databento", "IBKR", "Hybrid Live"]


def _count_quoted(chain: pd.DataFrame) -> int:
    """Rows in the chain with at least one usable bid or ask quote."""
    empty = pd.Series(dtype=float)
    bid = pd.to_numeric(chain.get("bid_px_00", empty), errors="coerce")
    ask = pd.to_numeric(chain.get("ask_px_00", empty), errors="coerce")
    return int(((bid.notna() & (bid > 0)) | (ask.notna() & (ask > 0))).sum())


_COMMON = ["raw_symbol", "expiration", "right", "strike", "mid", "iv"]
_BASIC_GREEKS = ["delta", "gamma", "vega", "theta"]
_HIGHER_GREEKS = ["vanna", "charm", "vomma", "veta", "speed", "color", "zomma"]
_TAIL_GREEKS = ["rho", "epsilon", "vera", "ultima"]

VIEW_COLUMNS = {
    "Basic": ["raw_symbol", "expiration", "right", "strike", "bid_px_00", "ask_px_00", "mid", "iv"] + _BASIC_GREEKS,
    "Higher Order": _COMMON + _BASIC_GREEKS + _HIGHER_GREEKS,
    "Full": _COMMON + _BASIC_GREEKS + _HIGHER_GREEKS + _TAIL_GREEKS,
}
DEFAULT_VIEW = "Basic"

_COLUMN_WIDTHS = {
    "raw_symbol": 180, "expiration": 90, "right": 50, "strike": 70,
    "bid_px_00": 70, "ask_px_00": 70, "mid": 70, "iv": 64,
    "delta": 64, "gamma": 64, "vega": 64, "theta": 64,
    "rho": 64, "epsilon": 64,
    "vanna": 66, "charm": 64, "vomma": 70, "veta": 66, "vera": 66,
    "speed": 70, "zomma": 66, "color": 64, "ultima": 70,
}
# Trader-screen scaling (raw math units → conventional display units)
_TRADER_SCALES = trader_unit_scales()
# Per-column decimal places for display
_DECIMALS = {
    "strike": 1, "bid_px_00": 2, "ask_px_00": 2, "mid": 2,
    "iv": 4, "delta": 4, "gamma": 6, "vega": 4, "theta": 4,
    "rho": 4, "epsilon": 4,
    "vanna": 5, "charm": 5, "vomma": 5, "veta": 6, "vera": 6,
    "speed": 7, "zomma": 5, "color": 6, "ultima": 6,
}


class MstrOptionsWorkstation:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MSTR Options Workstation")
        self.root.geometry("1480x880")
        self.root.minsize(1200, 720)
        self.chain = pd.DataFrame()

        self.underlying_var = tk.StringVar(value="MSTR")
        # Spot default: latest available MSTR close from Databento OHLCV-1d.
        # Refresh manually if you reopen the app days later, or pick Hybrid Live
        # to auto-update from IB on chain load.
        self.spot_var = tk.StringVar(value="178.06")
        self.rate_var = tk.StringVar(value="0.045")
        self.query_date_var = tk.StringVar(value=(date.today() - timedelta(days=2)).isoformat())
        self.start_time_var = tk.StringVar(value=f"{date.today() - timedelta(days=2)}T15:30:00-04:00")
        self.end_time_var = tk.StringVar(value=f"{date.today() - timedelta(days=2)}T15:35:00-04:00")
        # 0 (or empty) means unlimited; 5000 default = effectively unlimited for any equity
        self.max_symbols_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="Set DATABENTO_API_KEY for real data, or use Sample Mode.")
        self.sample_mode_var = tk.BooleanVar(value=not bool(os.getenv("DATABENTO_API_KEY")))
        # Data source selector: Sample / Databento / IBKR
        default_source = "Sample" if not bool(os.getenv("DATABENTO_API_KEY")) else "Databento"
        self.data_source_var = tk.StringVar(value=default_source)
        self.ibkr_host_var = tk.StringVar(value="127.0.0.1")
        self.ibkr_port_var = tk.StringVar(value="7497")  # TWS paper
        self.expiry_var = tk.StringVar(value="All")
        self.greek_view_var = tk.StringVar(value=DEFAULT_VIEW)
        self.display_columns: list[str] = list(VIEW_COLUMNS[DEFAULT_VIEW])
        self.contracts_metric_var = tk.StringVar(value="0")
        self.expiries_metric_var = tk.StringVar(value="0")
        self.avg_iv_metric_var = tk.StringVar(value="-")
        self.atm_metric_var = tk.StringVar(value="-")

        # PDF tab state
        self.pdf_expiry_var = tk.StringVar(value="")
        self.pdf_show_lognormal_var = tk.BooleanVar(value=True)
        self.pdf_show_heston_var = tk.BooleanVar(value=True)
        self.pdf_status_var = tk.StringVar(value="Load a chain, then pick an expiry and compute.")
        self.pdf_distribution: ImpliedDistribution | None = None
        # Heston calibration state
        self.heston_result: CalibrationResult | None = None
        # Cache: (expiry_date, K_array, pdf_array)
        self._heston_pdf_cache: tuple | None = None

        # Vol surface tab state — view selector + display options
        self.vol_view_var = tk.StringVar(value="3D Surface")
        self.vol_show_points_var = tk.BooleanVar(value=True)
        self.vol_z_var = tk.StringVar(value="IV")  # IV or Total Variance
        self.vol_cmap_var = tk.StringVar(value="viridis")

        # Vol smile tab state
        self.smile_expiry_var = tk.StringVar(value="")
        self.smile_xaxis_var = tk.StringVar(value="log-moneyness")
        self.smile_show_svi_var = tk.BooleanVar(value=True)
        self.smile_show_heston_var = tk.BooleanVar(value=False)
        self.smile_show_market_var = tk.BooleanVar(value=True)

        # Vol profile (term structure) tab state
        self.profile_show_atm_var = tk.BooleanVar(value=True)
        self.profile_show_25d_var = tk.BooleanVar(value=True)
        self.profile_show_10d_var = tk.BooleanVar(value=False)
        self.profile_xaxis_var = tk.StringVar(value="years")

        # Chain breadth — controls IB / Hybrid Live data pulls. "All" = no expiry cap.
        self.expiry_count_var = tk.StringVar(value="All")
        self.strike_window_var = tk.StringVar(value="0.40")

        self._build_ui()

    def _build_ui(self) -> None:
        self._configure_style()
        self._configure_matplotlib_defaults()
        self.root.configure(bg="#070b14")

        shell = ttk.Frame(self.root, style="App.TFrame", padding=0)
        shell.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(shell, bg="#0a0f1c", height=88)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Accent gradient stripe along the top — gives the header a "product" feel.
        # Two thin frames in different blues approximate a subtle gradient.
        tk.Frame(header, bg="#38bdf8", height=2).pack(fill=tk.X, side=tk.TOP)
        tk.Frame(header, bg="#0ea5e9", height=1).pack(fill=tk.X, side=tk.TOP)

        title_block = tk.Frame(header, bg="#0a0f1c")
        title_block.pack(side=tk.LEFT, fill=tk.Y, padx=28, pady=12)

        # Title row with an accent dot — adds a small product-mark feel
        title_row = tk.Frame(title_block, bg="#0a0f1c")
        title_row.pack(anchor=tk.W)
        tk.Label(
            title_row, text="●", bg="#0a0f1c", fg="#38bdf8",
            font=("Segoe UI", 14, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 8))
        tk.Label(
            title_row,
            text="MSTR Options Workstation",
            bg="#0a0f1c",
            fg="#f1f5f9",
            font=("Segoe UI", 21, "bold"),
        ).pack(side=tk.LEFT)

        tk.Label(
            title_block,
            text="OPRA chain  ·  IV surface  ·  Smile  ·  Term Structure  ·  Heston / B-L densities",
            bg="#0a0f1c",
            fg="#64748b",
            font=("Segoe UI", 9),
        ).pack(anchor=tk.W, pady=(4, 0))

        # Right-side: live source badge + a small clock to feel "alive"
        right_block = tk.Frame(header, bg="#0a0f1c")
        right_block.pack(side=tk.RIGHT, padx=28)
        self.source_badge = tk.Label(
            right_block,
            text=self.data_source_var.get().upper(),
            bg="#1e293b",
            fg="#38bdf8",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=6,
        )
        self.source_badge.pack(side=tk.TOP, anchor=tk.E)
        self.data_source_var.trace_add(
            "write",
            lambda *_: self.source_badge.configure(text=self.data_source_var.get().upper()),
        )
        self.clock_var = tk.StringVar(value=datetime.now().strftime("%a  %b %d  %H:%M"))
        tk.Label(
            right_block, textvariable=self.clock_var,
            bg="#0a0f1c", fg="#64748b", font=("Segoe UI", 9),
        ).pack(side=tk.TOP, anchor=tk.E, pady=(6, 0))
        self._tick_clock()

        body = ttk.Frame(shell, style="App.TFrame", padding=(16, 14, 16, 12))
        body.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(body, style="App.TFrame")
        top.pack(fill=tk.X)

        controls = ttk.Frame(top, style="Panel.TFrame", padding=14)
        controls.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))

        self._entry(controls, "Underlying", self.underlying_var, 0, 0, 9)
        self._entry(controls, "Spot", self.spot_var, 0, 2, 10)
        self._entry(controls, "Rate", self.rate_var, 0, 4, 10)
        self._entry(controls, "Definition Date", self.query_date_var, 0, 6, 14)
        ttk.Label(controls, text="Expiries", style="FieldLabel.TLabel").grid(row=0, column=8, padx=(4, 5), pady=5, sticky=tk.W)
        ttk.Combobox(
            controls, textvariable=self.expiry_count_var,
            values=["All", "4", "6", "8", "12", "16"],
            width=6, state="readonly", style="App.TCombobox",
        ).grid(row=0, column=9, padx=(0, 8), pady=5, sticky=tk.W)
        self._entry(controls, "Quote Start", self.start_time_var, 1, 0, 24)
        self._entry(controls, "Quote End", self.end_time_var, 1, 2, 24)
        self._entry(controls, "Max Symbols", self.max_symbols_var, 1, 4, 10)

        ttk.Label(controls, text="Source", style="FieldLabel.TLabel").grid(row=1, column=6, padx=(0, 5), pady=5, sticky=tk.W)
        ttk.Combobox(
            controls, textvariable=self.data_source_var, values=DATA_SOURCES,
            width=10, state="readonly", style="App.TCombobox",
        ).grid(row=1, column=7, padx=(0, 8), pady=5, sticky=tk.W)
        ttk.Label(controls, text="K Win %", style="FieldLabel.TLabel").grid(row=1, column=8, padx=(4, 5), pady=5, sticky=tk.W)
        ttk.Entry(controls, textvariable=self.strike_window_var, width=6).grid(row=1, column=9, padx=(0, 8), pady=5, sticky=tk.W)
        ttk.Label(controls, text="IB Port", style="FieldLabel.TLabel").grid(row=1, column=10, padx=(4, 5), pady=5, sticky=tk.W)
        ttk.Entry(controls, textvariable=self.ibkr_port_var, width=6).grid(row=1, column=11, padx=(0, 8), pady=5, sticky=tk.W)

        actions = ttk.Frame(top, style="Panel.TFrame", padding=14)
        actions.pack(side=tk.RIGHT, fill=tk.Y)
        ttk.Button(actions, text="Load Chain", command=self.load_chain, style="Primary.TButton").pack(fill=tk.X, ipady=4)
        ttk.Button(actions, text="Estimate Cost", command=self.estimate_quote_cost, style="Secondary.TButton").pack(fill=tk.X, ipady=4, pady=(10, 0))

        metric_strip = ttk.Frame(body, style="App.TFrame")
        metric_strip.pack(fill=tk.X, pady=(12, 12))
        self._metric_card(metric_strip, "Contracts", self.contracts_metric_var, "#38bdf8").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self._metric_card(metric_strip, "Expirations", self.expiries_metric_var, "#a78bfa").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        # ATM IV is the natural front-month ATM number a trader would quote.
        # Previously we showed a vega-weighted mean across delta∈[0.15,0.85]; for
        # MSTR's steep skew that blends in 100%+ wing strikes and exceeds 100%,
        # which is confusing as a top-line metric. ATM IV stays bounded near ~60-70%.
        self._metric_card(metric_strip, "ATM IV (front)", self.avg_iv_metric_var, "#22c55e").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self._metric_card(metric_strip, "ATM Strike", self.atm_metric_var, "#f59e0b").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Tabbed area — Chain table + Implied PDF + Vol family (Surface / Smile / Profile)
        self.notebook = ttk.Notebook(body)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        chain_tab = ttk.Frame(self.notebook, style="App.TFrame")
        self.notebook.add(chain_tab, text="  Chain  ")
        self._build_chain_tab(chain_tab)

        pdf_tab = ttk.Frame(self.notebook, style="App.TFrame")
        self.notebook.add(pdf_tab, text="  Implied PDF  ")
        self._build_pdf_tab(pdf_tab)

        vol_tab = ttk.Frame(self.notebook, style="App.TFrame")
        self.notebook.add(vol_tab, text="  Vol Surface  ")
        self._build_vol_surface_tab(vol_tab)

        smile_tab = ttk.Frame(self.notebook, style="App.TFrame")
        self.notebook.add(smile_tab, text="  Vol Smile  ")
        self._build_vol_smile_tab(smile_tab)

        profile_tab = ttk.Frame(self.notebook, style="App.TFrame")
        self.notebook.add(profile_tab, text="  Vol Profile  ")
        self._build_vol_profile_tab(profile_tab)

        status = ttk.Label(body, textvariable=self.status_var, anchor=tk.W, style="Status.TLabel")
        status.pack(fill=tk.X, pady=(8, 0))

    def _build_chain_tab(self, parent: ttk.Frame) -> None:
        filters = ttk.Frame(parent, style="Panel.TFrame", padding=(12, 9))
        filters.pack(fill=tk.X, pady=(0, 1))
        ttk.Label(filters, text="Expiration", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        self.expiry_combo = ttk.Combobox(filters, textvariable=self.expiry_var, values=["All"], width=14, state="readonly", style="App.TCombobox")
        self.expiry_combo.pack(side=tk.LEFT, padx=(8, 18))
        self.expiry_combo.bind("<<ComboboxSelected>>", lambda _event: self.refresh_table())

        ttk.Label(filters, text="Greek View", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        self.greek_view_combo = ttk.Combobox(
            filters,
            textvariable=self.greek_view_var,
            values=list(VIEW_COLUMNS.keys()),
            width=14,
            state="readonly",
            style="App.TCombobox",
        )
        self.greek_view_combo.pack(side=tk.LEFT, padx=(8, 12))
        self.greek_view_combo.bind("<<ComboboxSelected>>", lambda _event: self._on_greek_view_change())

        ttk.Button(filters, text="Refresh View", command=self.refresh_table, style="Secondary.TButton").pack(side=tk.LEFT)

        table_frame = ttk.Frame(parent, style="TableWrap.TFrame", padding=1)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.table = ttk.Treeview(table_frame, columns=self.display_columns, show="headings", style="Chain.Treeview")
        yscroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        xscroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.table.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self._configure_table_columns()

        # call / put coloring is light enough to read on dark rows
        self.table.tag_configure("call", foreground="#4ade80")
        self.table.tag_configure("put", foreground="#f87171")
        self.table.tag_configure("odd", background=self._PAL["ROW_ODD"])
        self.table.tag_configure("even", background=self._PAL["ROW_EVEN"])

    def _build_pdf_tab(self, parent: ttk.Frame) -> None:
        controls = ttk.Frame(parent, style="Panel.TFrame", padding=(12, 9))
        controls.pack(fill=tk.X, pady=(0, 1))

        ttk.Label(controls, text="Expiry", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        self.pdf_expiry_combo = ttk.Combobox(
            controls,
            textvariable=self.pdf_expiry_var,
            values=[],
            width=14,
            state="readonly",
            style="App.TCombobox",
        )
        self.pdf_expiry_combo.pack(side=tk.LEFT, padx=(8, 18))
        # Auto-recompute when the user picks a different expiry (no need to
        # click Compute PDF a second time). Heston curve auto-updates via
        # the cache invalidating on expiry change inside _redraw_pdf_chart.
        self.pdf_expiry_combo.bind("<<ComboboxSelected>>", lambda _event: self.compute_pdf())

        ttk.Checkbutton(
            controls, text="Lognormal",
            variable=self.pdf_show_lognormal_var,
            command=self._redraw_pdf_chart,
            style="App.TCheckbutton",
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Checkbutton(
            controls, text="Heston",
            variable=self.pdf_show_heston_var,
            command=self._redraw_pdf_chart,
            style="App.TCheckbutton",
        ).pack(side=tk.LEFT, padx=(0, 18))

        ttk.Button(controls, text="Compute PDF", command=self.compute_pdf, style="Primary.TButton").pack(side=tk.LEFT, ipady=2, padx=(0, 8))
        ttk.Button(controls, text="Calibrate Heston", command=self.run_heston_calibration, style="Secondary.TButton").pack(side=tk.LEFT, ipady=2)

        pdf_status = ttk.Label(controls, textvariable=self.pdf_status_var, style="PanelLabel.TLabel")
        pdf_status.pack(side=tk.LEFT, padx=(18, 0))

        main = ttk.Frame(parent, style="App.TFrame")
        main.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        chart_wrap = ttk.Frame(main, style="TableWrap.TFrame", padding=1)
        chart_wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        self.pdf_figure = Figure(figsize=(9.0, 6.8), dpi=118, facecolor="#0b1220")
        gs = self.pdf_figure.add_gridspec(2, 1, height_ratios=[3, 1.6], hspace=0.32)
        self.pdf_ax = self.pdf_figure.add_subplot(gs[0])
        self.smile_ax = self.pdf_figure.add_subplot(gs[1])
        self._render_pdf_placeholder()
        self.pdf_canvas = FigureCanvasTkAgg(self.pdf_figure, master=chart_wrap)
        self.pdf_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar_frame = ttk.Frame(chart_wrap, style="App.TFrame")
        toolbar_frame.pack(fill=tk.X)
        self.pdf_toolbar = NavigationToolbar2Tk(self.pdf_canvas, toolbar_frame)
        self.pdf_toolbar.update()

        stats_wrap = tk.Frame(
            main, bg=self._PAL["BG_PANEL"], highlightthickness=1,
            highlightbackground=self._PAL["BORDER"], width=290,
        )
        stats_wrap.pack(side=tk.RIGHT, fill=tk.Y)
        stats_wrap.pack_propagate(False)
        tk.Frame(stats_wrap, bg=self._PAL["ACCENT"], height=3).pack(fill=tk.X)
        tk.Label(
            stats_wrap, text="SUMMARY STATS", bg=self._PAL["BG_PANEL"],
            fg=self._PAL["FG_MUTED"], font=("Segoe UI", 9, "bold"),
        ).pack(anchor=tk.W, padx=14, pady=(12, 6))
        self.pdf_stats_text = tk.Text(
            stats_wrap, bg=self._PAL["BG_PANEL"], fg=self._PAL["FG_TEXT"],
            font=("Consolas", 10), relief="flat", borderwidth=0,
            padx=14, pady=4, wrap="none", height=24,
            insertbackground=self._PAL["ACCENT"],
            selectbackground=self._PAL["ROW_SEL"], selectforeground="#f8fafc",
        )
        self.pdf_stats_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 8))
        self.pdf_stats_text.insert("1.0", "(no distribution computed yet)")
        self.pdf_stats_text.configure(state="disabled")

    def _render_pdf_placeholder(self) -> None:
        for ax, text in (
            (self.pdf_ax, "Load a chain, pick an expiry, click Compute PDF."),
            (self.smile_ax, "Smile fit appears here once a PDF is computed."),
        ):
            ax.clear()
            ax.set_facecolor("#0b1220")
            ax.text(
                0.5, 0.5, text,
                ha="center", va="center", transform=ax.transAxes,
                color="#64748b", fontsize=11, fontstyle="italic",
            )
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)

    # ===== Vol Surface tab (3D Surface + Heatmap) =====
    def _build_vol_surface_tab(self, parent: ttk.Frame) -> None:
        controls = ttk.Frame(parent, style="Panel.TFrame", padding=(12, 9))
        controls.pack(fill=tk.X, pady=(0, 1))

        ttk.Label(controls, text="View", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        view_combo = ttk.Combobox(
            controls, textvariable=self.vol_view_var,
            values=["3D Surface", "Heatmap"],
            width=14, state="readonly", style="App.TCombobox",
        )
        view_combo.pack(side=tk.LEFT, padx=(8, 18))
        view_combo.bind("<<ComboboxSelected>>", lambda _e: self.refresh_vol_surface())

        ttk.Label(controls, text="Z", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        z_combo = ttk.Combobox(
            controls, textvariable=self.vol_z_var,
            values=["IV", "Total Variance"],
            width=14, state="readonly", style="App.TCombobox",
        )
        z_combo.pack(side=tk.LEFT, padx=(8, 18))
        z_combo.bind("<<ComboboxSelected>>", lambda _e: self.refresh_vol_surface())

        ttk.Label(controls, text="Colormap", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        cmap_combo = ttk.Combobox(
            controls, textvariable=self.vol_cmap_var,
            values=["viridis", "plasma", "magma", "inferno", "cividis", "turbo", "RdYlBu_r", "Spectral_r"],
            width=10, state="readonly", style="App.TCombobox",
        )
        cmap_combo.pack(side=tk.LEFT, padx=(8, 18))
        cmap_combo.bind("<<ComboboxSelected>>", lambda _e: self.refresh_vol_surface())

        ttk.Checkbutton(
            controls, text="Market points", variable=self.vol_show_points_var,
            command=self.refresh_vol_surface, style="App.TCheckbutton",
        ).pack(side=tk.LEFT, padx=(0, 18))

        ttk.Button(
            controls, text="Refresh", command=self.refresh_vol_surface,
            style="Secondary.TButton",
        ).pack(side=tk.LEFT, ipady=2)

        self.vol_status_var = tk.StringVar(value="Load a chain, then pick a view.")
        ttk.Label(controls, textvariable=self.vol_status_var, style="PanelLabel.TLabel").pack(side=tk.LEFT, padx=(18, 0))

        wrap = ttk.Frame(parent, style="TableWrap.TFrame", padding=1)
        wrap.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        # Larger figure + bumped DPI for crisper text/lines (rcParams set this too,
        # but Figure() explicit dpi wins when the global default is overridden)
        self.vol_figure = Figure(figsize=(10.2, 7.0), dpi=118, facecolor="#0b1220")
        self.vol_canvas = FigureCanvasTkAgg(self.vol_figure, master=wrap)
        self.vol_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self._vol_ax = None
        self._vol_cbar = None
        self._render_vol_placeholder()

        tb_frame = ttk.Frame(wrap, style="App.TFrame")
        tb_frame.pack(fill=tk.X)
        self.vol_toolbar = NavigationToolbar2Tk(self.vol_canvas, tb_frame)
        self.vol_toolbar.update()

    def _render_vol_placeholder(self) -> None:
        self.vol_figure.clear()
        self._vol_cbar = None
        ax = self.vol_figure.add_subplot(111)
        ax.set_facecolor("#0b1220")
        ax.text(
            0.5, 0.5, "Load a chain · pick a view · click Refresh.",
            transform=ax.transAxes, ha="center", va="center",
            color="#94a3b8", fontsize=12, fontstyle="italic",
        )
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        self._vol_ax = ax
        self.vol_canvas.draw_idle()

    def _build_surface_grid(self, df_iv: pd.DataFrame, spot: float, rate: float):
        """Fit SVI per expiry, evaluate on a uniform (k, T) mesh.

        Returns
        -------
        (k_grid, T_arr, IV_mesh, market_pts, n_fits, slice_ranges)
            k_grid     : 1D log-moneyness grid (uniform)
            T_arr      : 1D maturities (years)
            IV_mesh    : 2D (n_T, n_k) implied vols — NaN where outside per-expiry obs range
            market_pts : (k_obs, T_obs, iv_obs) flattened market scatter
            n_fits     : how many slices got an SVI fit
            slice_ranges: dict T -> (k_min_obs, k_max_obs) for the mask
        """
        from mstr_options_lab.surface.svi import fit_svi_slice, svi_iv

        expiries = sorted(df_iv["T"].unique())
        k_obs_all, T_obs_all, iv_obs_all = [], [], []
        slices: dict[float, tuple[np.ndarray, np.ndarray, object]] = {}  # T -> (k, iv, svi_or_None)
        slice_ranges: dict[float, tuple[float, float]] = {}
        k_lo_global, k_hi_global = +np.inf, -np.inf
        n_fits = 0

        for T_val in expiries:
            slc = df_iv[df_iv["T"] == T_val].sort_values("strike")
            if slc.empty:
                continue
            F = spot * np.exp(rate * T_val)
            k = np.log(slc["strike"].to_numpy(dtype=float) / F)
            iv = slc["iv_num"].to_numpy(dtype=float)
            k_obs_all.append(k); T_obs_all.append(np.full_like(k, T_val)); iv_obs_all.append(iv)
            slice_ranges[T_val] = (float(k.min()), float(k.max()))
            k_lo_global = min(k_lo_global, float(k.min()))
            k_hi_global = max(k_hi_global, float(k.max()))
            svi = None
            if len(slc) >= 5:
                try:
                    svi = fit_svi_slice(k, iv, T=T_val)
                    n_fits += 1
                except Exception:
                    svi = None
            slices[T_val] = (k, iv, svi)

        if not np.isfinite(k_lo_global) or not np.isfinite(k_hi_global) or k_hi_global <= k_lo_global:
            return None

        # Pad the global k-range slightly for visual breathing room
        pad = 0.03 * (k_hi_global - k_lo_global)
        k_grid = np.linspace(k_lo_global - pad, k_hi_global + pad, 80)
        T_arr = np.array(expiries, dtype=float)
        IV_mesh = np.full((len(T_arr), len(k_grid)), np.nan)

        for i, T_val in enumerate(T_arr):
            k, iv, svi = slices[T_val]
            k_min, k_max = slice_ranges[T_val]
            # Slight extrapolation tolerance per slice — keeps the surface filled
            # near the observed wings without painting fiction far past them.
            tol = 0.10 * max(k_max - k_min, 0.1)
            mask = (k_grid >= k_min - tol) & (k_grid <= k_max + tol)
            if svi is not None:
                IV_mesh[i, mask] = svi_iv(k_grid[mask], T_val, svi)
            elif k.size >= 2:
                # Too few strikes for SVI; linear-in-k interp within the obs range
                inside = mask & (k_grid >= k_min) & (k_grid <= k_max)
                IV_mesh[i, inside] = np.interp(k_grid[inside], k, iv)

        market_pts = (
            np.concatenate(k_obs_all) if k_obs_all else np.array([]),
            np.concatenate(T_obs_all) if T_obs_all else np.array([]),
            np.concatenate(iv_obs_all) if iv_obs_all else np.array([]),
        )
        return k_grid, T_arr, IV_mesh, market_pts, n_fits, slice_ranges

    def refresh_vol_surface(self) -> None:
        """Render the IV surface — SVI-fitted rectangular mesh + market scatter.

        View selector controls rendering mode:
          • 3D Surface     — plot_surface with viridis colormap, market points overlay
          • Heatmap        — pcolormesh in (k, T) space
          • Term Structure — ATM IV / 25Δ wings vs T
        """
        if self.chain.empty:
            self.vol_status_var.set("Load a chain first.")
            return

        try:
            spot = float(self.spot_var.get())
            rate = float(self.rate_var.get())
        except ValueError:
            self.vol_status_var.set("Bad spot/rate.")
            return

        # Filter to rows with valid IV + Greeks — guarantees pipeline integrity
        df = self.chain.copy()
        df["iv_num"] = pd.to_numeric(df["iv"], errors="coerce")
        df["vega_num"] = pd.to_numeric(df.get("vega", pd.Series(dtype=float)), errors="coerce")
        df = df[df["iv_num"].notna()]
        if "vega" in df.columns:
            df = df[df["vega_num"].notna() & (df["vega_num"] > 0)]
        if df.empty:
            self.vol_status_var.set("No strikes with computed Greeks. Try a different source.")
            self._render_vol_placeholder()
            return

        df["T"] = df["days_to_expiry"].astype(float) / 365.0
        df = df[df["T"] > 1e-4]  # drop same-day expiries (degenerate)
        df_iv = df.groupby(["expiration", "T", "strike"], as_index=False)["iv_num"].mean()
        if df_iv.empty:
            self.vol_status_var.set("No usable strikes after filtering.")
            self._render_vol_placeholder()
            return

        built = self._build_surface_grid(df_iv, spot, rate)
        if built is None:
            self.vol_status_var.set("Couldn't build surface grid.")
            self._render_vol_placeholder()
            return
        k_grid, T_arr, IV_mesh, market_pts, n_fits, slice_ranges = built

        # Z-axis units
        z_mode = self.vol_z_var.get()
        if z_mode == "Total Variance":
            Z = IV_mesh ** 2 * T_arr[:, None]
            z_label = "total variance  w = σ²·T"
            mk_z = market_pts[2] ** 2 * market_pts[1]
        else:
            Z = IV_mesh * 100.0
            z_label = "IV (%)"
            mk_z = market_pts[2] * 100.0

        view = self.vol_view_var.get()
        cmap_name = self.vol_cmap_var.get() or "viridis"

        # Clear figure fully so we can switch between 3D and 2D sub-grids.
        # Term structure used to live here; it's now in the Vol Profile tab.
        self.vol_figure.clear()
        self._vol_cbar = None
        self.vol_figure.patch.set_facecolor("#0b1220")

        if view == "Heatmap":
            self._render_vol_heatmap(k_grid, T_arr, Z, market_pts, cmap_name, z_label, slice_ranges)
        else:
            self._render_vol_3d(k_grid, T_arr, Z, market_pts, mk_z, cmap_name, z_label)

        self.vol_status_var.set(
            f"{len(df_iv)} strikes · {len(T_arr)} expiries · {n_fits} SVI fits · view: {view}"
        )
        self.vol_canvas.draw_idle()

    def _render_vol_3d(self, k_grid, T_arr, Z, market_pts, mk_z, cmap_name, z_label) -> None:
        ax = self.vol_figure.add_subplot(111, projection="3d")
        ax.set_facecolor("#0b1220")
        K_mesh, T_mesh = np.meshgrid(k_grid, T_arr)

        # plot_surface needs no NaNs in the Z array — fall back to row-mean fill
        Z_filled = np.where(np.isnan(Z), np.nanmean(Z), Z)
        z_lo = float(np.nanmin(Z))
        z_hi = float(np.nanmax(Z))
        if not np.isfinite(z_lo) or not np.isfinite(z_hi) or z_hi <= z_lo:
            z_lo, z_hi = 0.0, 1.0

        surf = ax.plot_surface(
            K_mesh, T_mesh, Z_filled,
            cmap=cmap_name, vmin=z_lo, vmax=z_hi,
            edgecolor="none", linewidth=0, antialiased=True,
            rcount=min(len(T_arr) * 4, 80), ccount=min(len(k_grid), 80),
            alpha=0.92, shade=True,
        )

        if self.vol_show_points_var.get() and market_pts[0].size:
            ax.scatter(
                market_pts[0], market_pts[1], mk_z,
                c="#f8fafc", s=14, alpha=0.85, edgecolors="#0f172a", linewidths=0.4,
                depthshade=True, label=f"Market ({market_pts[0].size})",
            )

        # Cosmetics — dark theme axes
        for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
            axis.pane.fill = True
            axis.pane.set_facecolor("#111827")
            axis.pane.set_edgecolor("#1e293b")
            axis.label.set_color("#cbd5e1")
        ax.tick_params(colors="#94a3b8", labelsize=8)
        ax.set_xlabel("log-moneyness  k = ln(K / F)", color="#cbd5e1", labelpad=6)
        ax.set_ylabel("T (years)", color="#cbd5e1", labelpad=6)
        ax.set_zlabel(z_label, color="#cbd5e1", labelpad=6)
        ax.set_title(
            f"{self.underlying_var.get().upper()}  ·  implied volatility surface",
            color="#f8fafc", fontsize=13, fontweight="bold", pad=12,
        )
        ax.view_init(elev=24, azim=-58)
        try:
            ax.set_box_aspect((1.5, 1.2, 0.85))
        except Exception:
            pass

        cbar = self.vol_figure.colorbar(surf, ax=ax, shrink=0.65, pad=0.08, aspect=22)
        cbar.set_label(z_label, color="#cbd5e1")
        cbar.ax.yaxis.set_tick_params(color="#94a3b8", labelsize=8)
        for t in cbar.ax.get_yticklabels():
            t.set_color("#cbd5e1")
        self._vol_cbar = cbar

    def _render_vol_heatmap(self, k_grid, T_arr, Z, market_pts, cmap_name, z_label, slice_ranges) -> None:
        ax = self.vol_figure.add_subplot(111)
        ax.set_facecolor("#0b1220")

        # Use shading="auto" so unequal cell sizes (we have non-uniform T spacing)
        # render without complaints. Mask NaN cells.
        Z_ma = np.ma.masked_invalid(Z)
        # Build edge arrays for pcolormesh — midpoints between sorted T's
        T_edges = np.zeros(len(T_arr) + 1)
        if len(T_arr) >= 2:
            T_edges[1:-1] = 0.5 * (T_arr[:-1] + T_arr[1:])
            T_edges[0] = T_arr[0] - (T_arr[1] - T_arr[0]) / 2
            T_edges[-1] = T_arr[-1] + (T_arr[-1] - T_arr[-2]) / 2
        else:
            T_edges = np.array([T_arr[0] * 0.9, T_arr[0] * 1.1])
        dk = k_grid[1] - k_grid[0]
        k_edges = np.concatenate(([k_grid[0] - dk / 2], k_grid + dk / 2))

        pcm = ax.pcolormesh(k_edges, T_edges, Z_ma, cmap=cmap_name, shading="auto")
        cbar = self.vol_figure.colorbar(pcm, ax=ax, pad=0.02)
        cbar.set_label(z_label, color="#cbd5e1")
        cbar.ax.yaxis.set_tick_params(color="#94a3b8", labelsize=8)
        for t in cbar.ax.get_yticklabels():
            t.set_color("#cbd5e1")
        self._vol_cbar = cbar

        if self.vol_show_points_var.get() and market_pts[0].size:
            ax.scatter(
                market_pts[0], market_pts[1],
                c="#f8fafc", s=12, alpha=0.7, edgecolors="#0f172a", linewidths=0.4,
            )

        ax.axvline(0.0, color="#94a3b8", linewidth=0.7, linestyle=":", alpha=0.7)
        ax.set_xlabel("log-moneyness  k = ln(K / F)", color="#cbd5e1")
        ax.set_ylabel("T (years)", color="#cbd5e1")
        ax.set_title(
            f"{self.underlying_var.get().upper()}  ·  IV heatmap",
            color="#f8fafc", fontsize=13, fontweight="bold", pad=10,
        )
        ax.tick_params(colors="#94a3b8", labelsize=9)
        for spine in ax.spines.values():
            spine.set_color("#334155")

    # ===== Vol Smile tab =====
    def _build_vol_smile_tab(self, parent: ttk.Frame) -> None:
        controls = ttk.Frame(parent, style="Panel.TFrame", padding=(12, 9))
        controls.pack(fill=tk.X, pady=(0, 1))

        ttk.Label(controls, text="Expiry", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        self.smile_expiry_combo = ttk.Combobox(
            controls, textvariable=self.smile_expiry_var, values=[],
            width=14, state="readonly", style="App.TCombobox",
        )
        self.smile_expiry_combo.pack(side=tk.LEFT, padx=(8, 18))
        self.smile_expiry_combo.bind("<<ComboboxSelected>>", lambda _e: self.refresh_vol_smile())

        ttk.Label(controls, text="X-axis", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        xaxis_combo = ttk.Combobox(
            controls, textvariable=self.smile_xaxis_var,
            values=["log-moneyness", "strike"],
            width=14, state="readonly", style="App.TCombobox",
        )
        xaxis_combo.pack(side=tk.LEFT, padx=(8, 18))
        xaxis_combo.bind("<<ComboboxSelected>>", lambda _e: self.refresh_vol_smile())

        ttk.Checkbutton(controls, text="Market", variable=self.smile_show_market_var,
                        command=self.refresh_vol_smile, style="App.TCheckbutton").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Checkbutton(controls, text="SVI", variable=self.smile_show_svi_var,
                        command=self.refresh_vol_smile, style="App.TCheckbutton").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Checkbutton(controls, text="Heston", variable=self.smile_show_heston_var,
                        command=self.refresh_vol_smile, style="App.TCheckbutton").pack(side=tk.LEFT, padx=(0, 18))

        ttk.Button(controls, text="Refresh", command=self.refresh_vol_smile,
                   style="Secondary.TButton").pack(side=tk.LEFT, ipady=2)

        self.smile_status_var = tk.StringVar(value="Load a chain, pick an expiry.")
        ttk.Label(controls, textvariable=self.smile_status_var, style="PanelLabel.TLabel").pack(side=tk.LEFT, padx=(18, 0))

        main = ttk.Frame(parent, style="App.TFrame")
        main.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        chart_wrap = ttk.Frame(main, style="TableWrap.TFrame", padding=1)
        chart_wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        self.smile_figure = Figure(figsize=(10.0, 6.6), dpi=118, facecolor="#0b1220")
        self.smile_ax_main = self.smile_figure.add_subplot(111)
        self.smile_canvas = FigureCanvasTkAgg(self.smile_figure, master=chart_wrap)
        self.smile_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self._render_smile_placeholder()
        tb_frame = ttk.Frame(chart_wrap, style="App.TFrame")
        tb_frame.pack(fill=tk.X)
        self.smile_toolbar = NavigationToolbar2Tk(self.smile_canvas, tb_frame)
        self.smile_toolbar.update()

        # Side panel — SVI params + smile diagnostics
        stats_wrap = tk.Frame(
            main, bg=self._PAL["BG_PANEL"], highlightthickness=1,
            highlightbackground=self._PAL["BORDER"], width=290,
        )
        stats_wrap.pack(side=tk.RIGHT, fill=tk.Y)
        stats_wrap.pack_propagate(False)
        tk.Frame(stats_wrap, bg=self._PAL["ACCENT"], height=3).pack(fill=tk.X)
        tk.Label(
            stats_wrap, text="SMILE DIAGNOSTICS", bg=self._PAL["BG_PANEL"],
            fg=self._PAL["FG_MUTED"], font=("Segoe UI", 9, "bold"),
        ).pack(anchor=tk.W, padx=14, pady=(12, 6))
        self.smile_stats_text = tk.Text(
            stats_wrap, bg=self._PAL["BG_PANEL"], fg=self._PAL["FG_TEXT"],
            font=("Consolas", 10), relief="flat", borderwidth=0,
            padx=14, pady=4, wrap="none", height=24,
            insertbackground=self._PAL["ACCENT"],
            selectbackground=self._PAL["ROW_SEL"], selectforeground="#f8fafc",
        )
        self.smile_stats_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 8))
        self.smile_stats_text.insert("1.0", "(no expiry computed yet)")
        self.smile_stats_text.configure(state="disabled")

    def _render_smile_placeholder(self) -> None:
        ax = self.smile_ax_main
        ax.clear()
        ax.set_facecolor("#0b1220")
        ax.text(
            0.5, 0.5, "Load a chain · pick an expiry · click Refresh.",
            transform=ax.transAxes, ha="center", va="center",
            color="#94a3b8", fontsize=12, fontstyle="italic",
        )
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.grid(False)
        self.smile_canvas.draw_idle()

    def refresh_vol_smile(self) -> None:
        """Render the smile for the selected expiry: market dots, SVI fit, optional Heston."""
        from mstr_options_lab.surface.svi import fit_svi_slice, svi_iv

        if self.chain.empty:
            self.smile_status_var.set("Load a chain first.")
            return
        sel = self.smile_expiry_var.get()
        if not sel:
            self.smile_status_var.set("Pick an expiry.")
            return
        try:
            expiry = datetime.strptime(sel, "%Y-%m-%d").date()
        except ValueError:
            self.smile_status_var.set(f"Bad expiry: {sel}")
            return

        try:
            spot = float(self.spot_var.get())
            rate = float(self.rate_var.get())
        except ValueError:
            self.smile_status_var.set("Bad spot/rate.")
            return

        df = self.chain.copy()
        df["iv_num"] = pd.to_numeric(df["iv"], errors="coerce")
        df = df[(df["expiration"].astype(str) == sel) & df["iv_num"].notna()]
        if df.empty:
            self.smile_status_var.set(f"No IV data for {sel}.")
            self._render_smile_placeholder()
            return

        # Days to expiry — needed for SVI total-variance scaling
        today = date.today()
        T = max((expiry - today).days, 1) / 365.0
        F = spot * np.exp(rate * T)

        # Build per-strike OTM IV (avg of call+put where both exist; otherwise take what's there)
        per_strike = df.groupby("strike", as_index=False).agg(iv_num=("iv_num", "mean"))
        per_strike = per_strike.sort_values("strike")
        K_arr = per_strike["strike"].to_numpy(dtype=float)
        iv_arr = per_strike["iv_num"].to_numpy(dtype=float)
        k_arr = np.log(K_arr / F)

        svi = None
        if len(K_arr) >= 5:
            try:
                svi = fit_svi_slice(k_arr, iv_arr, T=T)
            except Exception:
                svi = None

        # Dense fit curve
        k_lo = float(k_arr.min()) - 0.05
        k_hi = float(k_arr.max()) + 0.05
        k_dense = np.linspace(k_lo, k_hi, 240)
        K_dense = F * np.exp(k_dense)

        self.smile_figure.clear()
        self.smile_figure.patch.set_facecolor("#0b1220")
        ax = self.smile_figure.add_subplot(111)
        ax.set_facecolor("#0b1220")
        self.smile_ax_main = ax

        x_mode = self.smile_xaxis_var.get()
        x_obs = k_arr if x_mode == "log-moneyness" else K_arr
        x_dense = k_dense if x_mode == "log-moneyness" else K_dense
        x_atm = 0.0 if x_mode == "log-moneyness" else F

        # Market dots
        if self.smile_show_market_var.get():
            ax.scatter(x_obs, iv_arr * 100, s=44, color="#38bdf8",
                       edgecolors="#0b1220", linewidths=0.8, zorder=5,
                       label=f"Market ({len(x_obs)})")

        # SVI curve
        if svi is not None and self.smile_show_svi_var.get():
            iv_svi = svi_iv(k_dense, T, svi)
            ax.plot(x_dense, iv_svi * 100, color="#a78bfa", linewidth=2.1,
                    label="SVI fit")

        # Heston smile via FFT pricing then Black inversion (one-shot)
        if self.smile_show_heston_var.get() and self.heston_result is not None:
            try:
                C_h = fft_prices_many_strikes(
                    heston_cf, spot, K_dense, T, rate, 0.0,
                    self.heston_result.params, right="call",
                )
                iv_h = bs_implied_vol(C_h, spot, K_dense, T, rate, "call", 0.0)
                ok = ~np.isnan(iv_h)
                if ok.any():
                    ax.plot(x_dense[ok], np.asarray(iv_h)[ok] * 100,
                            color="#f97316", linestyle="-.", linewidth=1.8,
                            label="Heston")
            except Exception:
                pass

        ax.axvline(x_atm, color="#22c55e", linestyle="--", linewidth=1.1, alpha=0.7,
                   label=("k = 0" if x_mode == "log-moneyness" else f"Forward {F:.1f}"))

        ax.set_xlabel("log-moneyness  k = ln(K / F)" if x_mode == "log-moneyness"
                      else "Strike K",
                      color="#cbd5e1")
        ax.set_ylabel("Implied volatility  σ(K)  (%)", color="#cbd5e1")
        ax.set_title(
            f"{self.underlying_var.get().upper()}  ·  IV smile  ·  expiry {sel}  "
            f"·  T = {int(T * 365)}d  ·  F = {F:.1f}",
            color="#f1f5f9", fontsize=12, fontweight="bold",
        )
        ax.legend(loc="best")

        self.smile_figure.tight_layout()
        self.smile_canvas.draw_idle()

        # Diagnostics panel
        self._update_smile_stats(K_arr, iv_arr, k_arr, T, F, svi)
        self.smile_status_var.set(
            f"{len(K_arr)} strikes · T = {int(T*365)}d · {'SVI fit OK' if svi else 'SVI fit skipped'}"
        )

    def _update_smile_stats(self, K_arr, iv_arr, k_arr, T, F, svi) -> None:
        """Compute ATM IV, ATM slope, ATM curvature, 25Δ skew, wing levels."""
        from mstr_options_lab.surface.svi import svi_iv

        # ATM via interpolation at k = 0
        if k_arr.min() <= 0 <= k_arr.max() and len(k_arr) >= 2:
            atm_iv = float(np.interp(0.0, k_arr, iv_arr))
        else:
            atm_iv = float(iv_arr[np.argmin(np.abs(k_arr))])

        # ATM slope and curvature — finite differences on SVI curve if available
        if svi is not None:
            k_fine = np.linspace(-0.02, 0.02, 21)
            iv_fine = svi_iv(k_fine, T, svi)
            dk = k_fine[1] - k_fine[0]
            slope = float((iv_fine[11] - iv_fine[9]) / (2 * dk))
            curv = float((iv_fine[12] - 2 * iv_fine[10] + iv_fine[8]) / dk ** 2)

            # 25Δ wings: |k| ≈ 0.5 · ATM IV · √T (BS approximation)
            kt = 0.5 * atm_iv * np.sqrt(max(T, 1e-6))
            iv_call25 = float(svi_iv(np.array([+kt]), T, svi)[0])
            iv_put25 = float(svi_iv(np.array([-kt]), T, svi)[0])
        else:
            slope = curv = float("nan")
            iv_call25 = iv_put25 = float("nan")

        rr_25d = iv_call25 - iv_put25  # risk reversal (calls − puts)
        bf_25d = 0.5 * (iv_call25 + iv_put25) - atm_iv  # butterfly

        lines = [
            f"Forward       {F:>10.2f}",
            f"T             {T*365:>8.0f} d",
            f"Strikes       {len(K_arr):>10d}",
            f"K range       {K_arr.min():>5.0f} - {K_arr.max():.0f}",
            "",
            "ATM",
            f"  IV          {atm_iv:>10.2%}",
            f"  Slope ∂σ/∂k {slope:>+10.4f}",
            f"  Curvature   {curv:>+10.4f}",
            "",
            "25Δ WINGS  (approx.)",
            f"  Call IV     {iv_call25:>10.2%}",
            f"  Put  IV     {iv_put25:>10.2%}",
            f"  Risk Rev.   {rr_25d:>+10.2%}",
            f"  Butterfly   {bf_25d:>+10.2%}",
        ]
        if svi is not None:
            lines += [
                "",
                "SVI PARAMS",
                f"  a           {svi.a:>+8.4f}",
                f"  b           {svi.b:>+8.4f}",
                f"  rho         {svi.rho:>+8.4f}",
                f"  m           {svi.m:>+8.4f}",
                f"  sigma       {svi.sigma:>+8.4f}",
            ]
        if self.heston_result is not None and self.smile_show_heston_var.get():
            hp = self.heston_result.params
            lines += [
                "",
                "HESTON (joint fit)",
                f"  kappa       {hp.kappa:>+8.4f}",
                f"  theta       {hp.theta:>+8.4f}",
                f"  sigma       {hp.sigma:>+8.4f}",
                f"  rho         {hp.rho:>+8.4f}",
                f"  v0          {hp.v0:>+8.4f}",
                f"  RMSE        {self.heston_result.rmse_iv_pct:>7.2f} vp",
            ]
        self.smile_stats_text.configure(state="normal")
        self.smile_stats_text.delete("1.0", tk.END)
        self.smile_stats_text.insert("1.0", "\n".join(lines))
        self.smile_stats_text.configure(state="disabled")

    # ===== Vol Profile (term structure) tab =====
    def _build_vol_profile_tab(self, parent: ttk.Frame) -> None:
        controls = ttk.Frame(parent, style="Panel.TFrame", padding=(12, 9))
        controls.pack(fill=tk.X, pady=(0, 1))

        ttk.Label(controls, text="X-axis", style="PanelLabel.TLabel").pack(side=tk.LEFT)
        x_combo = ttk.Combobox(
            controls, textvariable=self.profile_xaxis_var,
            values=["years", "days"],
            width=10, state="readonly", style="App.TCombobox",
        )
        x_combo.pack(side=tk.LEFT, padx=(8, 18))
        x_combo.bind("<<ComboboxSelected>>", lambda _e: self.refresh_vol_profile())

        ttk.Checkbutton(controls, text="ATM IV", variable=self.profile_show_atm_var,
                        command=self.refresh_vol_profile, style="App.TCheckbutton").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Checkbutton(controls, text="25Δ wings", variable=self.profile_show_25d_var,
                        command=self.refresh_vol_profile, style="App.TCheckbutton").pack(side=tk.LEFT, padx=(0, 6))
        ttk.Checkbutton(controls, text="10Δ wings", variable=self.profile_show_10d_var,
                        command=self.refresh_vol_profile, style="App.TCheckbutton").pack(side=tk.LEFT, padx=(0, 18))

        ttk.Button(controls, text="Refresh", command=self.refresh_vol_profile,
                   style="Secondary.TButton").pack(side=tk.LEFT, ipady=2)

        self.profile_status_var = tk.StringVar(value="Load a chain.")
        ttk.Label(controls, textvariable=self.profile_status_var, style="PanelLabel.TLabel").pack(side=tk.LEFT, padx=(18, 0))

        main = ttk.Frame(parent, style="App.TFrame")
        main.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        chart_wrap = ttk.Frame(main, style="TableWrap.TFrame", padding=1)
        chart_wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        self.profile_figure = Figure(figsize=(10.0, 6.6), dpi=118, facecolor="#0b1220")
        # Two stacked axes: top = ATM + wings, bottom = forward-vol bars
        gs = self.profile_figure.add_gridspec(2, 1, height_ratios=[2.2, 1.0], hspace=0.30)
        self.profile_ax_top = self.profile_figure.add_subplot(gs[0])
        self.profile_ax_bot = self.profile_figure.add_subplot(gs[1])
        self._render_profile_placeholder()
        self.profile_canvas = FigureCanvasTkAgg(self.profile_figure, master=chart_wrap)
        self.profile_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        tb_frame = ttk.Frame(chart_wrap, style="App.TFrame")
        tb_frame.pack(fill=tk.X)
        self.profile_toolbar = NavigationToolbar2Tk(self.profile_canvas, tb_frame)
        self.profile_toolbar.update()

        # Side panel — per-expiry table
        stats_wrap = tk.Frame(
            main, bg=self._PAL["BG_PANEL"], highlightthickness=1,
            highlightbackground=self._PAL["BORDER"], width=290,
        )
        stats_wrap.pack(side=tk.RIGHT, fill=tk.Y)
        stats_wrap.pack_propagate(False)
        tk.Frame(stats_wrap, bg=self._PAL["ACCENT"], height=3).pack(fill=tk.X)
        tk.Label(
            stats_wrap, text="TERM STRUCTURE", bg=self._PAL["BG_PANEL"],
            fg=self._PAL["FG_MUTED"], font=("Segoe UI", 9, "bold"),
        ).pack(anchor=tk.W, padx=14, pady=(12, 6))
        self.profile_stats_text = tk.Text(
            stats_wrap, bg=self._PAL["BG_PANEL"], fg=self._PAL["FG_TEXT"],
            font=("Consolas", 9), relief="flat", borderwidth=0,
            padx=10, pady=4, wrap="none", height=28,
            insertbackground=self._PAL["ACCENT"],
            selectbackground=self._PAL["ROW_SEL"], selectforeground="#f8fafc",
        )
        self.profile_stats_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 8))
        self.profile_stats_text.insert("1.0", "(no profile computed yet)")
        self.profile_stats_text.configure(state="disabled")

    def _render_profile_placeholder(self) -> None:
        for ax, msg in (
            (self.profile_ax_top, "Load a chain to see ATM IV and wing term structure."),
            (self.profile_ax_bot, "Forward-vol bars appear here once a profile is built."),
        ):
            ax.clear()
            ax.set_facecolor("#0b1220")
            ax.text(0.5, 0.5, msg, transform=ax.transAxes, ha="center", va="center",
                    color="#64748b", fontsize=11, fontstyle="italic")
            ax.set_xticks([]); ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.grid(False)

    def refresh_vol_profile(self) -> None:
        """ATM + 25Δ + 10Δ wing IV vs T, plus forward-vol bars below."""
        if self.chain.empty:
            self.profile_status_var.set("Load a chain first.")
            return
        try:
            spot = float(self.spot_var.get())
            rate = float(self.rate_var.get())
        except ValueError:
            self.profile_status_var.set("Bad spot/rate.")
            return

        df = self.chain.copy()
        df["iv_num"] = pd.to_numeric(df["iv"], errors="coerce")
        df = df[df["iv_num"].notna()]
        if df.empty:
            self.profile_status_var.set("No IV in chain.")
            self._render_profile_placeholder()
            self.profile_canvas.draw_idle()
            return
        df["T"] = df["days_to_expiry"].astype(float) / 365.0
        df = df[df["T"] > 1e-4]

        built = self._build_surface_grid(
            df.groupby(["expiration", "T", "strike"], as_index=False)["iv_num"].mean(),
            spot, rate,
        )
        if built is None:
            self.profile_status_var.set("Couldn't build term structure.")
            self._render_profile_placeholder()
            self.profile_canvas.draw_idle()
            return
        k_grid, T_arr, IV_mesh, _, n_fits, _ = built

        # Sample ATM, 25Δ, 10Δ from each slice via interpolation on the fitted curve
        # 25Δ: |k| ≈ 0.5 · σ · √T   ;  10Δ: |k| ≈ 1.28 · σ · √T  (BS approx.)
        atm = np.full(len(T_arr), np.nan)
        c25 = np.full(len(T_arr), np.nan); p25 = np.full(len(T_arr), np.nan)
        c10 = np.full(len(T_arr), np.nan); p10 = np.full(len(T_arr), np.nan)
        for i, T_val in enumerate(T_arr):
            iv_row = IV_mesh[i]
            ok = ~np.isnan(iv_row)
            if not ok.any():
                continue
            atm[i] = float(np.interp(0.0, k_grid[ok], iv_row[ok]))
            sqrtT = np.sqrt(max(T_val, 1e-6))
            kt25 = 0.5 * atm[i] * sqrtT
            kt10 = 1.28 * atm[i] * sqrtT
            c25[i] = float(np.interp(+kt25, k_grid[ok], iv_row[ok]))
            p25[i] = float(np.interp(-kt25, k_grid[ok], iv_row[ok]))
            c10[i] = float(np.interp(+kt10, k_grid[ok], iv_row[ok]))
            p10[i] = float(np.interp(-kt10, k_grid[ok], iv_row[ok]))

        # X-axis units
        x_mode = self.profile_xaxis_var.get()
        x = T_arr if x_mode == "years" else (T_arr * 365.0)
        x_label = "T (years)" if x_mode == "years" else "Days to expiry"

        self.profile_figure.clear()
        self.profile_figure.patch.set_facecolor("#0b1220")
        gs = self.profile_figure.add_gridspec(2, 1, height_ratios=[2.2, 1.0], hspace=0.30)
        ax_top = self.profile_figure.add_subplot(gs[0])
        ax_bot = self.profile_figure.add_subplot(gs[1])
        self.profile_ax_top = ax_top
        self.profile_ax_bot = ax_bot
        for ax in (ax_top, ax_bot):
            ax.set_facecolor("#0b1220")

        # Top panel: ATM and wings
        if self.profile_show_10d_var.get():
            ax_top.fill_between(x, p10 * 100, c10 * 100, color="#f97316", alpha=0.10)
            ax_top.plot(x, c10 * 100, color="#f97316", linewidth=1.3, linestyle=":", marker="^",
                        markersize=4, label="10Δ call")
            ax_top.plot(x, p10 * 100, color="#f97316", linewidth=1.3, linestyle=":", marker="v",
                        markersize=4, label="10Δ put")
        if self.profile_show_25d_var.get():
            ax_top.fill_between(x, p25 * 100, c25 * 100, color="#38bdf8", alpha=0.12)
            ax_top.plot(x, c25 * 100, color="#22c55e", linewidth=1.5, linestyle="--", marker="^",
                        markersize=5, label="25Δ call")
            ax_top.plot(x, p25 * 100, color="#fb7185", linewidth=1.5, linestyle="--", marker="v",
                        markersize=5, label="25Δ put")
        if self.profile_show_atm_var.get():
            ax_top.plot(x, atm * 100, color="#38bdf8", linewidth=2.4, marker="o",
                        markersize=6, label="ATM IV", zorder=5)

        ax_top.set_xlabel(x_label)
        ax_top.set_ylabel("Implied volatility  σ  (%)")
        ax_top.set_title(
            f"{self.underlying_var.get().upper()}  ·  IV term structure  ·  "
            f"{len(T_arr)} expiries  ·  {n_fits} SVI fits",
        )
        ax_top.legend(loc="best", ncol=2)

        # Bottom panel: implied forward variance / forward vol between consecutive expiries
        # Forward variance: σ²(T2)·T2 − σ²(T1)·T1 = σ_fwd² · (T2 − T1)
        atm_clean = np.where(np.isnan(atm), np.nan, atm)
        fwd_vol = np.full(len(T_arr), np.nan)
        for i in range(len(T_arr)):
            if i == 0:
                fwd_vol[i] = atm_clean[i]
            else:
                T1, T2 = T_arr[i - 1], T_arr[i]
                if np.isnan(atm_clean[i]) or np.isnan(atm_clean[i - 1]) or T2 <= T1:
                    continue
                var_fwd = (atm_clean[i] ** 2 * T2 - atm_clean[i - 1] ** 2 * T1) / (T2 - T1)
                fwd_vol[i] = np.sqrt(max(var_fwd, 1e-8))

        # Colour bars green where forward vol < spot vol (contango / "term up"),
        # orange where forward vol > spot vol (backwardation in vol — typically a stress signal).
        colors_bar = np.where(fwd_vol > atm_clean, "#f97316", "#22c55e")
        width = (x[-1] - x[0]) / max(len(x) - 1, 1) * 0.55 if len(x) > 1 else 0.05
        ax_bot.bar(x, fwd_vol * 100, color=colors_bar, alpha=0.85, width=width,
                   edgecolor="#0b1220", linewidth=0.4)
        ax_bot.plot(x, atm * 100, color="#cbd5e1", linewidth=1.2, linestyle="-",
                    alpha=0.7, label="Spot vol (ATM)")

        ax_bot.set_xlabel(x_label)
        ax_bot.set_ylabel("Forward vol (%)")
        ax_bot.set_title("Implied forward vol between consecutive expiries",
                         fontsize=10, fontweight="bold", pad=6)
        ax_bot.legend(loc="best", fontsize=8)

        self.profile_canvas.draw_idle()

        # Side panel: per-expiry table
        self._update_profile_stats(T_arr, atm, c25, p25, fwd_vol)
        self.profile_status_var.set(
            f"{len(T_arr)} expiries · {n_fits} SVI fits · DTE range "
            f"{int(T_arr.min()*365)}-{int(T_arr.max()*365)}d"
        )

    def _update_profile_stats(self, T_arr, atm, c25, p25, fwd_vol) -> None:
        lines = [
            f"{'DTE':>5} {'ATM':>6} {'25Δc':>6} {'25Δp':>6} {'RR':>6} {'FVol':>6}",
            "-" * 42,
        ]
        for i, T_val in enumerate(T_arr):
            dte = int(T_val * 365)
            atm_s = f"{atm[i]*100:.1f}" if np.isfinite(atm[i]) else "  -"
            c_s = f"{c25[i]*100:.1f}" if np.isfinite(c25[i]) else "  -"
            p_s = f"{p25[i]*100:.1f}" if np.isfinite(p25[i]) else "  -"
            rr = (c25[i] - p25[i]) * 100 if np.isfinite(c25[i]) and np.isfinite(p25[i]) else float("nan")
            rr_s = f"{rr:+.1f}" if np.isfinite(rr) else "  -"
            fv_s = f"{fwd_vol[i]*100:.1f}" if np.isfinite(fwd_vol[i]) else "  -"
            lines.append(f"{dte:>5} {atm_s:>6} {c_s:>6} {p_s:>6} {rr_s:>6} {fv_s:>6}")
        self.profile_stats_text.configure(state="normal")
        self.profile_stats_text.delete("1.0", tk.END)
        self.profile_stats_text.insert("1.0", "\n".join(lines))
        self.profile_stats_text.configure(state="disabled")

    def _tick_clock(self) -> None:
        """Update the header clock every 30 seconds — cheap, just reads system time."""
        try:
            self.clock_var.set(datetime.now().strftime("%a  %b %d  %H:%M"))
        except Exception:
            pass
        self.root.after(30_000, self._tick_clock)

    def _configure_matplotlib_defaults(self) -> None:
        """Pin global rcParams so every figure in the app gets the same polished look.

        Bumps DPI from 100 → 118 for crisper text/lines on modern monitors, and
        enables clean grids + a dark-theme-aware default cycle.
        """
        import matplotlib as mpl
        mpl.rcParams.update({
            "figure.dpi":          118,
            "savefig.dpi":         150,
            "figure.facecolor":    "#0b1220",
            "axes.facecolor":      "#0b1220",
            "axes.edgecolor":      "#334155",
            "axes.labelcolor":     "#cbd5e1",
            "axes.titlecolor":     "#f1f5f9",
            "axes.titlesize":      12,
            "axes.titleweight":    "bold",
            "axes.titlepad":       10,
            "axes.labelsize":      10,
            "axes.linewidth":      0.8,
            "axes.grid":           True,
            "grid.color":          "#1e293b",
            "grid.linestyle":      ":",
            "grid.linewidth":      0.6,
            "grid.alpha":          0.85,
            "xtick.color":         "#94a3b8",
            "ytick.color":         "#94a3b8",
            "xtick.labelsize":     9,
            "ytick.labelsize":     9,
            "xtick.direction":     "out",
            "ytick.direction":     "out",
            "lines.linewidth":     1.8,
            "lines.antialiased":   True,
            "patch.antialiased":   True,
            "font.family":         "Segoe UI",
            "font.size":           10,
            "legend.frameon":      True,
            "legend.facecolor":    "#0f172a",
            "legend.edgecolor":    "#334155",
            "legend.fontsize":     9,
            "legend.labelcolor":   "#cbd5e1",
            "text.color":          "#cbd5e1",
        })

    def _configure_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        # Palette (deeper slate + electric blue accent — pro-trader feel with more
        # contrast against panels than the old palette).
        BG_DEEP    = "#070b14"   # window + outer chrome (deeper than before)
        BG_PANEL   = "#0f172a"   # control panels (slightly lifted)
        BG_CHROME  = "#1e293b"   # subtle dividers / table headings
        BG_FIELD   = "#1e293b"   # entries / combobox fields
        FG_TEXT    = "#e2e8f0"   # primary text
        FG_MUTED   = "#94a3b8"   # secondary text / labels
        ACCENT     = "#38bdf8"   # primary accent
        ACCENT_HOV = "#0ea5e9"
        BORDER     = "#1e293b"   # softer than before — feels less boxy
        ROW_ODD    = "#0b1220"
        ROW_EVEN   = "#0f172a"
        ROW_SEL    = "#1e3a5f"

        style.configure("App.TFrame", background=BG_DEEP)
        style.configure("Panel.TFrame", background=BG_PANEL, relief="flat", borderwidth=0)
        style.configure("TableWrap.TFrame", background=BORDER)
        style.configure("PanelLabel.TLabel", background=BG_PANEL, foreground=FG_MUTED,
                        font=("Segoe UI", 9, "bold"))
        style.configure("FieldLabel.TLabel", background=BG_PANEL, foreground=FG_MUTED,
                        font=("Segoe UI", 8, "bold"))
        style.configure("Status.TLabel", background=BG_DEEP, foreground=FG_MUTED,
                        font=("Segoe UI", 9))

        style.configure(
            "TEntry",
            fieldbackground=BG_FIELD, foreground=FG_TEXT,
            bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
            insertcolor=ACCENT, padding=5,
        )
        style.map("TEntry",
                  bordercolor=[("focus", ACCENT)],
                  lightcolor=[("focus", ACCENT)],
                  darkcolor=[("focus", ACCENT)])

        style.configure(
            "App.TCombobox",
            fieldbackground=BG_FIELD, background=BG_FIELD, foreground=FG_TEXT,
            bordercolor=BORDER, arrowcolor=ACCENT, padding=5,
            selectbackground=BG_FIELD, selectforeground=FG_TEXT,
        )
        style.map("App.TCombobox",
                  fieldbackground=[("readonly", BG_FIELD)],
                  foreground=[("readonly", FG_TEXT)],
                  bordercolor=[("focus", ACCENT)])

        style.configure("App.TCheckbutton", background=BG_PANEL, foreground=FG_TEXT,
                        font=("Segoe UI", 9), focuscolor=BG_PANEL)
        style.map("App.TCheckbutton",
                  background=[("active", BG_PANEL)],
                  foreground=[("active", ACCENT)])

        style.configure(
            "Primary.TButton",
            background=ACCENT, foreground="#0b1220", borderwidth=0,
            font=("Segoe UI", 10, "bold"), padding=(16, 8),
        )
        style.map("Primary.TButton",
                  background=[("active", ACCENT_HOV), ("pressed", "#0284c7")])

        style.configure(
            "Secondary.TButton",
            background=BG_CHROME, foreground=FG_TEXT, borderwidth=0,
            font=("Segoe UI", 9, "bold"), padding=(13, 7),
        )
        style.map("Secondary.TButton",
                  background=[("active", "#2c3a52"), ("pressed", "#334155")])

        # Treeview (chain table) — dark rows, subtle striping, accent selection
        style.configure(
            "Chain.Treeview",
            background=ROW_ODD,
            foreground=FG_TEXT,
            fieldbackground=ROW_ODD,
            rowheight=26,
            borderwidth=0,
            font=("Segoe UI", 9),
        )
        style.configure(
            "Chain.Treeview.Heading",
            background=BG_CHROME,
            foreground=ACCENT,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padding=(8, 9),
        )
        style.map(
            "Chain.Treeview.Heading",
            background=[("active", "#2c3a52")],
        )
        style.map(
            "Chain.Treeview",
            background=[("selected", ROW_SEL)],
            foreground=[("selected", "#f8fafc")],
        )

        # Notebook (tabs)
        style.configure("TNotebook", background=BG_DEEP, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_PANEL, foreground=FG_MUTED,
                        padding=(18, 9), font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map(
            "TNotebook.Tab",
            background=[("selected", BG_DEEP), ("active", BG_CHROME)],
            foreground=[("selected", ACCENT), ("active", FG_TEXT)],
        )

        # Scrollbars
        style.configure("Vertical.TScrollbar",
                        background=BG_PANEL, troughcolor=BG_DEEP,
                        bordercolor=BG_DEEP, arrowcolor=FG_MUTED)
        style.configure("Horizontal.TScrollbar",
                        background=BG_PANEL, troughcolor=BG_DEEP,
                        bordercolor=BG_DEEP, arrowcolor=FG_MUTED)

        # Stash palette as instance attrs so card builders can read them
        self._PAL = dict(
            BG_DEEP=BG_DEEP, BG_PANEL=BG_PANEL, BG_CHROME=BG_CHROME, BG_FIELD=BG_FIELD,
            FG_TEXT=FG_TEXT, FG_MUTED=FG_MUTED, ACCENT=ACCENT, ACCENT_HOV=ACCENT_HOV,
            BORDER=BORDER, ROW_ODD=ROW_ODD, ROW_EVEN=ROW_EVEN, ROW_SEL=ROW_SEL,
        )

    def _entry(self, parent: ttk.Frame, label: str, var: tk.StringVar, row: int, col: int, width: int) -> None:
        ttk.Label(parent, text=label, style="FieldLabel.TLabel").grid(row=row, column=col, padx=(0, 5), pady=5, sticky=tk.W)
        ttk.Entry(parent, textvariable=var, width=width).grid(row=row, column=col + 1, padx=(0, 14), pady=5, sticky=tk.W)

    def _metric_card(self, parent: ttk.Frame, label: str, value_var: tk.StringVar, accent: str) -> tk.Frame:
        bg = self._PAL["BG_PANEL"]
        card = tk.Frame(parent, bg=bg, highlightthickness=1, highlightbackground=self._PAL["BORDER"])
        tk.Frame(card, bg=accent, height=3).pack(fill=tk.X)
        inner = tk.Frame(card, bg=bg)
        inner.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
        tk.Label(inner, text=label.upper(), bg=bg, fg=self._PAL["FG_MUTED"],
                 font=("Segoe UI", 8, "bold")).pack(anchor=tk.W)
        tk.Label(inner, textvariable=value_var, bg=bg, fg=self._PAL["FG_TEXT"],
                 font=("Segoe UI", 19, "bold")).pack(anchor=tk.W, pady=(4, 0))
        return card

    def _run_background(self, label: str, func) -> None:
        self.status_var.set(label)

        def worker() -> None:
            # ib_insync and databento.Live both use asyncio internally; worker
            # threads don't get an event loop for free. Create one for this thread
            # before any data adapter runs.
            import asyncio
            asyncio.set_event_loop(asyncio.new_event_loop())
            try:
                result = func()
                self.root.after(0, lambda: self._finish_load(result))
            except Exception as exc:
                self.root.after(0, lambda: self._show_error(exc))

        threading.Thread(target=worker, daemon=True).start()

    def load_chain(self) -> None:
        # CRITICAL: snapshot all Tk vars on the MAIN thread before handing off
        # to the worker. Tk variable reads from worker threads are fragile and
        # can fail with "main thread is not in main loop" depending on backend.
        raw_max = self.max_symbols_var.get().strip()
        max_symbols = 0 if (raw_max == "" or raw_max == "0") else max(int(raw_max), 1)
        exp_sel = self.expiry_count_var.get().strip()
        max_expiries = None if exp_sel.lower() == "all" else max(int(exp_sel), 1)
        try:
            strike_window_pct = max(float(self.strike_window_var.get()), 0.05)
        except ValueError:
            strike_window_pct = 0.40
        params = {
            "underlying": self.underlying_var.get().strip().upper() or "MSTR",
            "spot": float(self.spot_var.get()),
            "rate": float(self.rate_var.get()),
            "max_symbols": max_symbols,  # 0 = unlimited
            "max_expiries": max_expiries,
            "strike_window_pct": strike_window_pct,
            "query_date": self.query_date_var.get(),
            "start_time": self.start_time_var.get(),
            "end_time": self.end_time_var.get(),
            "source": self.data_source_var.get(),
            "ibkr_host": self.ibkr_host_var.get(),
            "ibkr_port": int(self.ibkr_port_var.get()),
        }
        self._run_background(
            "Loading MSTR option chain...",
            lambda: self._load_chain_data(**params),
        )

    def _load_chain_data(
        self, *,
        underlying: str, spot: float, rate: float, max_symbols: int,
        max_expiries: int | None, strike_window_pct: float,
        query_date: str, start_time: str, end_time: str,
        source: str, ibkr_host: str, ibkr_port: int,
    ) -> pd.DataFrame:
        """Pure function of explicit params — no Tk var access, safe in worker thread."""
        as_of = datetime.fromisoformat(query_date).date()

        if source == "Sample":
            # Generate sample chain CENTERED ON THE CURRENT SPOT so the Greeks
            # actually make sense (deep OTM strikes around a misaligned spot
            # produce nonsense IVs of 300%+).
            return enrich_chain_with_quotes(
                sample_mstr_chain(as_of, spot=spot),
                pd.DataFrame(), spot=spot, rate=rate, as_of=as_of,
            )

        # Effective expiry cap — "All" maps to a generously high number so downstream
        # adapters that require an integer (IB / Live) still slice safely.
        eff_max_expiries = 1000 if max_expiries is None else int(max_expiries)

        if source == "IBKR":
            if not IB_INSYNC_AVAILABLE:
                raise RuntimeError("ib_insync not installed. Run: pip install ib_insync")
            cfg = IBKRConfig(host=ibkr_host, port=ibkr_port)
            today = date.today()
            with IBKRClient(cfg) as ib:
                chain = ib.fetch_option_chain(
                    underlying, max_expiries=eff_max_expiries,
                    strike_window_pct=float(strike_window_pct),
                    spot_hint=spot, as_of=today,
                )
            if chain.empty:
                return chain
            chain["mid"] = (pd.to_numeric(chain["bid_px_00"], errors="coerce")
                            + pd.to_numeric(chain["ask_px_00"], errors="coerce")) / 2.0
            return compute_chain_greeks(chain, spot=spot, rate=rate, inplace=True)

        if source == "Hybrid Live":
            if not IB_INSYNC_AVAILABLE:
                raise RuntimeError("ib_insync not installed. Run: pip install ib_insync")
            today = date.today()

            # Step 1: live spot from IB TWS
            ib_cfg = IBKRConfig(host=ibkr_host, port=ibkr_port)
            with IBKRClient(ib_cfg) as ib:
                ib_quote = ib.fetch_underlying_quote(underlying)
            live_spot = ib_quote.get("last") or ib_quote.get("close")
            if not live_spot or not np.isfinite(live_spot):
                raise RuntimeError(f"Could not get live spot from IB for {underlying}")

            # Step 2: live OPRA chain via Databento, centered on the IB spot
            db_client = DatabentoLiveClient()
            chain = db_client.fetch_option_chain(
                underlying, spot_hint=float(live_spot),
                max_expiries=eff_max_expiries,
                strike_window_pct=float(strike_window_pct),
                listen_seconds=10.0, as_of=today,
            )
            if chain.empty:
                return chain
            chain["mid"] = (pd.to_numeric(chain["bid_px_00"], errors="coerce")
                            + pd.to_numeric(chain["ask_px_00"], errors="coerce")) / 2.0
            # Push the live IB spot back to the UI field (main-thread-safe)
            self.root.after(0, lambda v=float(live_spot): self.spot_var.set(f"{v:.2f}"))
            return compute_chain_greeks(chain, spot=float(live_spot), rate=rate, inplace=True)

        # Databento (historical)
        config = DatabentoConfig()
        definitions = fetch_option_definitions(underlying=underlying, start=query_date, config=config)
        if definitions.empty:
            return definitions
        sorted_defs = definitions.assign(distance=(definitions["strike"] - spot).abs()).sort_values(["expiration", "distance"])
        # max_symbols == 0 → unlimited (pull all definitions). Otherwise top-N nearest.
        near_chain = sorted_defs if max_symbols == 0 else sorted_defs.head(max_symbols)
        symbols = near_chain["raw_symbol"].tolist()
        quote_limit = None if max_symbols == 0 else max_symbols * 50
        quotes = fetch_cmbp1_snapshot(
            symbols=symbols, start=start_time, end=end_time or None,
            config=config, limit=quote_limit,
        )
        return enrich_chain_with_quotes(near_chain.drop(columns=["distance"]), quotes, spot=spot, rate=rate, as_of=as_of)

    def _finish_load(self, chain: pd.DataFrame) -> None:
        self.chain = chain
        expiries = ["All"]
        pdf_expiries: list[str] = []
        if not chain.empty and "expiration" in chain.columns:
            sorted_exp = [str(exp) for exp in sorted(chain["expiration"].dropna().unique())]
            expiries.extend(sorted_exp)
            pdf_expiries = sorted_exp
        self.expiry_combo.configure(values=expiries)
        self.expiry_var.set(expiries[0])
        self.pdf_expiry_combo.configure(values=pdf_expiries)
        if pdf_expiries and not self.pdf_expiry_var.get():
            self.pdf_expiry_var.set(pdf_expiries[0])
        # New smile tab dropdown — same expiry list as PDF tab
        self.smile_expiry_combo.configure(values=pdf_expiries)
        if pdf_expiries and not self.smile_expiry_var.get():
            self.smile_expiry_var.set(pdf_expiries[0])
        # Invalidate Heston state since the chain has changed
        self.heston_result = None
        self._heston_pdf_cache = None
        self._update_metrics(chain)
        self.refresh_table()

        source = self.data_source_var.get()
        n_quoted = _count_quoted(chain) if not chain.empty else 0
        self.status_var.set(
            f"Loaded {len(chain)} contracts for {self.underlying_var.get().upper()} "
            f"(source: {source}, {n_quoted} with quotes)."
        )

        # Auto-refresh the vol family (surface / smile / profile) whenever a new chain lands
        if not chain.empty:
            for refresh_fn in (self.refresh_vol_surface, self.refresh_vol_smile, self.refresh_vol_profile):
                try:
                    refresh_fn()
                except Exception:
                    pass  # never block load completion on render glitches

        # Detect market-closed: live source returned a chain but every row has
        # NaN bid AND NaN ask. OPRA / IBKR silent on weekends / after-hours.
        if source in ("IBKR", "Hybrid Live") and not chain.empty and n_quoted == 0:
            messagebox.showwarning(
                "No live quotes",
                f"{source} returned {len(chain)} contracts but none have live quotes.\n\n"
                "Most likely cause: OPRA / IBKR market data is closed (weekend or "
                "after-hours). The underlying spot may still be cached, but option "
                "NBBOs aren't being broadcast.\n\n"
                "For weekend / off-hours work, try:\n"
                "  • Source = Sample  (synthetic chain, full Greeks)\n"
                "  • Source = Databento  (last trading day's OPRA snapshot)\n\n"
                "For live OPRA, try again during regular hours (9:30am-4:00pm ET)."
            )

    def _show_error(self, exc: Exception) -> None:
        self.status_var.set("Load failed.")
        messagebox.showerror("MSTR Options Workstation", str(exc))

    def _configure_table_columns(self) -> None:
        """Apply current ``self.display_columns`` to the Treeview heading + width set."""
        self.table.configure(columns=self.display_columns)
        text_cols = {"raw_symbol", "right", "expiration"}
        for col in self.display_columns:
            self.table.heading(col, text=col)
            self.table.column(
                col,
                width=_COLUMN_WIDTHS.get(col, 80),
                anchor=tk.W if col in text_cols else tk.E,
            )

    def _on_greek_view_change(self) -> None:
        view = self.greek_view_var.get()
        self.display_columns = list(VIEW_COLUMNS.get(view, VIEW_COLUMNS[DEFAULT_VIEW]))
        self._configure_table_columns()
        self.refresh_table()

    # ===== Implied PDF tab =====
    def compute_pdf(self) -> None:
        if self.chain.empty:
            self.pdf_status_var.set("Load a chain first.")
            return
        sel = self.pdf_expiry_var.get()
        if not sel:
            self.pdf_status_var.set("Pick an expiry.")
            return
        try:
            expiry = datetime.strptime(sel, "%Y-%m-%d").date()
        except ValueError:
            self.pdf_status_var.set(f"Bad expiry: {sel}")
            return

        self.pdf_status_var.set(f"Fitting SVI + computing density for {sel}...")

        def worker() -> None:
            try:
                dist = compute_implied_distribution(
                    self.chain, expiry,
                    spot=float(self.spot_var.get()),
                    rate=float(self.rate_var.get()),
                    as_of=date.today(),
                )
                self.root.after(0, lambda: self._on_pdf_ready(dist))
            except Exception as exc:
                self.root.after(0, lambda: self._on_pdf_error(exc))

        threading.Thread(target=worker, daemon=True).start()

    def _on_pdf_ready(self, dist: ImpliedDistribution) -> None:
        self.pdf_distribution = dist
        self.pdf_status_var.set(
            f"Fitted SVI to {dist.n_strikes_used} strikes  ·  ATM IV {dist.atm_iv:.1%}  ·  T = {dist.days_to_expiry}d"
        )
        self._redraw_pdf_chart()
        self._update_pdf_stats(dist)

    def _on_pdf_error(self, exc: Exception) -> None:
        self.pdf_status_var.set(f"PDF failed: {exc}")
        messagebox.showerror("Implied PDF", str(exc))

    def run_heston_calibration(self) -> None:
        if self.chain.empty:
            self.pdf_status_var.set("Load a chain first.")
            return
        try:
            spot = float(self.spot_var.get())
            rate = float(self.rate_var.get())
        except ValueError:
            self.pdf_status_var.set("Bad spot/rate.")
            return

        self.pdf_status_var.set("Calibrating Heston across the surface (joint fit)...")

        def worker() -> None:
            try:
                res = calibrate_heston(self.chain, spot=spot, rate=rate, as_of=date.today())
                self.root.after(0, lambda: self._on_heston_calibrated(res))
            except Exception as exc:
                self.root.after(0, lambda: self._on_heston_error(exc))

        threading.Thread(target=worker, daemon=True).start()

    def _on_heston_calibrated(self, res: CalibrationResult) -> None:
        self.heston_result = res
        self._heston_pdf_cache = None
        feller = "OK" if res.feller_ok else "violated"
        self.pdf_status_var.set(
            f"Heston: RMSE {res.rmse_iv_pct:.2f}vp  ·  {res.n_options} opts × {res.n_expiries} expiries  ·  Feller {feller}"
        )
        self._redraw_pdf_chart()
        if self.pdf_distribution is not None:
            self._update_pdf_stats(self.pdf_distribution)

    def _on_heston_error(self, exc: Exception) -> None:
        self.pdf_status_var.set(f"Heston calibration failed: {exc}")
        messagebox.showerror("Heston calibration", str(exc))

    def _heston_pdf_for_current_expiry(self, dist: ImpliedDistribution) -> tuple[np.ndarray, np.ndarray] | None:
        if self.heston_result is None:
            return None
        if self._heston_pdf_cache is not None and self._heston_pdf_cache[0] == dist.expiry:
            return self._heston_pdf_cache[1], self._heston_pdf_cache[2]
        T = dist.days_to_expiry / 365.0
        K_h, pdf_h, _ = heston_pdf_for_expiry(
            dist.spot, T, dist.rate, dist.dividend_yield, self.heston_result.params,
            K_min=float(dist.K[0]), K_max=float(dist.K[-1]), n_K=len(dist.K),
        )
        self._heston_pdf_cache = (dist.expiry, K_h, pdf_h)
        return K_h, pdf_h

    def _redraw_pdf_chart(self) -> None:
        dist = self.pdf_distribution
        ax = self.pdf_ax
        ax.clear()
        ax.set_facecolor("#0b1220")
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("#334155")

        if dist is None:
            self._render_pdf_placeholder()
            self.pdf_canvas.draw_idle()
            return

        K = dist.K
        pdf = dist.pdf

        # Lognormal baseline using fitted ATM IV  (BSM-flat-vol reference)
        if self.pdf_show_lognormal_var.get():
            T = dist.days_to_expiry / 365.0
            sigma = max(dist.atm_iv, 1e-6)
            scale = dist.spot * np.exp((dist.rate - dist.dividend_yield - 0.5 * sigma ** 2) * T)
            s = sigma * np.sqrt(T)
            ln_pdf = lognorm.pdf(K, s, scale=scale)
            ax.plot(K, ln_pdf, color="#94a3b8", linestyle="--", linewidth=1.6,
                    label=f"Lognormal (ATM IV={dist.atm_iv:.1%})")

        ax.plot(K, pdf, color="#38bdf8", linewidth=2.2, label="Implied PDF (SVI + B-L)")
        ax.fill_between(K, 0, pdf, color="#38bdf8", alpha=0.15)

        # Heston-implied PDF overlay (if calibrated)
        if self.pdf_show_heston_var.get() and self.heston_result is not None:
            heston = self._heston_pdf_for_current_expiry(dist)
            if heston is not None:
                K_h, pdf_h = heston
                ax.plot(
                    K_h, pdf_h, color="#f97316", linestyle="-.", linewidth=1.8,
                    label=f"Heston FFT (RMSE {self.heston_result.rmse_iv_pct:.2f}vp)",
                )

        ax.axvline(dist.spot, color="#22c55e", linestyle="-", linewidth=1.2,
                   label=f"Spot {dist.spot:.2f}")
        ax.axvline(dist.forward, color="#c084fc", linestyle="--", linewidth=1.0,
                   label=f"Forward {dist.forward:.2f}")
        ax.axvline(dist.p5, color="#f87171", linestyle=":", linewidth=1.0, alpha=0.85,
                   label=f"P5={dist.p5:.0f}")
        ax.axvline(dist.p95, color="#f87171", linestyle=":", linewidth=1.0, alpha=0.85,
                   label=f"P95={dist.p95:.0f}")
        ax.axvline(dist.p50, color="#38bdf8", linestyle=":", linewidth=1.0, alpha=0.6)

        ax.set_xlabel("S_T  (price at expiry)", color="#cbd5e1")
        ax.set_ylabel("density f(K)", color="#cbd5e1")
        title = (
            f"{self.underlying_var.get().upper()}  implied distribution  ·  "
            f"expiry {dist.expiry}  ·  {dist.days_to_expiry}d  ·  ATM IV {dist.atm_iv:.1%}"
        )
        ax.set_title(title, color="#f8fafc", fontsize=12, fontweight="bold", pad=10)
        leg = ax.legend(loc="upper right", fontsize=8, framealpha=0.85,
                        facecolor="#111827", edgecolor="#334155", labelcolor="#cbd5e1")
        ax.tick_params(colors="#94a3b8", labelsize=9)
        ax.grid(True, alpha=0.18, color="#334155", linestyle=":")

        # X-limit: zoom to where actual market data exists (strikes with computed Greeks),
        # not the full B-L K-grid (which extends to 5×F for moment integration).
        sub = self.chain[
            (self.chain["expiration"] == dist.expiry)
            & pd.to_numeric(self.chain["iv"], errors="coerce").notna()
        ]
        if not sub.empty:
            k_lo = float(sub["strike"].min())
            k_hi = float(sub["strike"].max())
            pad = max(0.02 * (k_hi - k_lo), 1.0)
            ax.set_xlim(k_lo - pad, k_hi + pad)
        else:
            ax.set_xlim(max(dist.K[0], dist.spot * 0.2), min(dist.K[-1], dist.spot * 3.0))

        # ===== Smile-fit subplot =====
        self._redraw_smile_subplot(dist)

        self.pdf_canvas.draw_idle()

    def _redraw_smile_subplot(self, dist: ImpliedDistribution) -> None:
        ax = self.smile_ax
        ax.clear()
        ax.set_facecolor("#0b1220")
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color("#334155")

        # Market OTM IVs (the actual smile we fit)
        k_obs, iv_obs = slice_to_otm_smile(self.chain, dist.expiry, forward=dist.forward)
        if k_obs.size:
            ax.scatter(k_obs, iv_obs * 100, color="#f8fafc",
                       edgecolors="#0b1220", linewidths=0.5,
                       s=24, zorder=5, label=f"Market OTM ({k_obs.size})")

        # Dense k-grid for the fit curves
        k_lo = float(min(k_obs.min(), -0.5) if k_obs.size else -0.5)
        k_hi = float(max(k_obs.max(), 0.5) if k_obs.size else 0.5)
        k_grid = np.linspace(k_lo - 0.1, k_hi + 0.1, 200)
        K_grid = dist.forward * np.exp(k_grid)
        T = dist.days_to_expiry / 365.0

        # SVI fit curve
        iv_svi = svi_iv(k_grid, T, dist.svi)
        ax.plot(k_grid, iv_svi * 100, color="#38bdf8", linewidth=1.8, label="SVI fit")

        # Heston-implied IVs (price via FFT, invert via fast Halley)
        if self.heston_result is not None and self.pdf_show_heston_var.get():
            try:
                C_heston = fft_prices_many_strikes(
                    heston_cf, dist.spot, K_grid, T, dist.rate, dist.dividend_yield,
                    self.heston_result.params, right="call",
                )
                iv_heston = bs_implied_vol(
                    C_heston, dist.spot, K_grid, T, dist.rate, "call", dist.dividend_yield,
                )
                ok = ~np.isnan(iv_heston)
                if ok.any():
                    ax.plot(
                        k_grid[ok], np.asarray(iv_heston)[ok] * 100,
                        color="#f97316", linestyle="-.", linewidth=1.6, label="Heston",
                    )
            except Exception:
                pass

        ax.axvline(0.0, color="#c084fc", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.set_xlabel("log-moneyness  k = ln(K / F)", color="#cbd5e1", fontsize=9)
        ax.set_ylabel("IV (%)", color="#cbd5e1", fontsize=9)
        ax.tick_params(colors="#94a3b8", labelsize=8)
        ax.grid(True, alpha=0.18, color="#334155", linestyle=":")
        ax.legend(loc="upper right", fontsize=7, framealpha=0.85,
                  facecolor="#111827", edgecolor="#334155", labelcolor="#cbd5e1")
        ax.set_title("Smile fit — market vs models", color="#f8fafc",
                     fontsize=10, fontweight="bold", pad=4)

    def _update_pdf_stats(self, dist: ImpliedDistribution) -> None:
        lines = [
            f"Expiry       {dist.expiry}",
            f"DTE          {dist.days_to_expiry} d",
            f"Spot         {dist.spot:>10.2f}",
            f"Forward      {dist.forward:>10.2f}",
            f"ATM IV       {dist.atm_iv:>10.2%}",
            f"Strikes used {dist.n_strikes_used:>10d}",
            "",
            "MOMENTS",
            f"Mean         {dist.mean:>10.2f}",
            f"Std          {dist.std:>10.2f}",
            f"Skewness     {dist.skew:>+10.3f}",
            f"Kurt (xs)    {dist.kurt_excess:>+10.3f}",
            "",
            "PERCENTILES",
            f"P5           {dist.p5:>10.2f}",
            f"P25          {dist.p25:>10.2f}",
            f"P50 (med)    {dist.p50:>10.2f}",
            f"P75          {dist.p75:>10.2f}",
            f"P95          {dist.p95:>10.2f}",
            "",
            f"90% range    {dist.p5:>6.0f} - {dist.p95:.0f}",
            f"  (rel)      {(dist.p5/dist.spot - 1):+.0%} / {(dist.p95/dist.spot - 1):+.0%}",
            "",
            "SVI PARAMS",
            f"  a          {dist.svi.a:>+8.4f}",
            f"  b          {dist.svi.b:>+8.4f}",
            f"  rho        {dist.svi.rho:>+8.4f}",
            f"  m          {dist.svi.m:>+8.4f}",
            f"  sigma      {dist.svi.sigma:>+8.4f}",
        ]
        if self.heston_result is not None:
            hp = self.heston_result.params
            lines += [
                "",
                "HESTON CALIBRATION",
                f"  kappa      {hp.kappa:>+8.4f}",
                f"  theta      {hp.theta:>+8.4f}  (vol {hp.theta ** 0.5:.1%})",
                f"  sigma      {hp.sigma:>+8.4f}",
                f"  rho        {hp.rho:>+8.4f}",
                f"  v0         {hp.v0:>+8.4f}  (vol {hp.v0 ** 0.5:.1%})",
                "",
                f"  RMSE       {self.heston_result.rmse_iv_pct:>7.2f} vp",
                f"  Options    {self.heston_result.n_options:>8d}",
                f"  Expiries   {self.heston_result.n_expiries:>8d}",
                f"  Feller     {'OK' if self.heston_result.feller_ok else 'VIOLATED':>8}",
            ]
        self.pdf_stats_text.configure(state="normal")
        self.pdf_stats_text.delete("1.0", tk.END)
        self.pdf_stats_text.insert("1.0", "\n".join(lines))
        self.pdf_stats_text.configure(state="disabled")

    def refresh_table(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)
        if self.chain.empty:
            return

        df = self.chain
        if self.expiry_var.get() != "All":
            df = df[df["expiration"].astype(str) == self.expiry_var.get()]

        for index, (_, row) in enumerate(df.sort_values(["expiration", "strike", "right"]).iterrows()):
            values = [self._format_cell(col, row.get(col)) for col in self.display_columns]
            tags = ["even" if index % 2 == 0 else "odd", str(row.get("right", ""))]
            self.table.insert("", tk.END, values=values, tags=tags)

    def _update_metrics(self, chain: pd.DataFrame) -> None:
        if chain.empty:
            self.contracts_metric_var.set("0")
            self.expiries_metric_var.set("0")
            self.avg_iv_metric_var.set("-")
            self.atm_metric_var.set("-")
            return

        self.contracts_metric_var.set(f"{len(chain):,}")
        self.expiries_metric_var.set(f"{chain['expiration'].nunique():,}" if "expiration" in chain.columns else "-")

        # ATM IV (front-month) — the natural reference value a trader quotes.
        # For each expiry, pick the strike closest to spot, take the call+put IV
        # average (where both exist), then return the front-month value. For MSTR
        # this typically sits in the 55-75% band; the old vega-weighted mean blended
        # in wing strikes that easily exceed 100% IV because of the steep skew.
        try:
            spot = float(self.spot_var.get())
        except ValueError:
            spot = float("nan")

        atm_iv_front = self._compute_atm_iv_front(chain, spot)
        if np.isfinite(atm_iv_front):
            self.avg_iv_metric_var.set(f"{atm_iv_front * 100:.1f}%")
        else:
            self.avg_iv_metric_var.set("-")

        if np.isfinite(spot) and "strike" in chain.columns and not chain.empty:
            atm = chain.assign(distance=(chain["strike"] - spot).abs()).sort_values("distance").iloc[0]
            self.atm_metric_var.set(f"{atm['strike']:.0f} {str(atm['right'])[0].upper()}")
        else:
            self.atm_metric_var.set("-")

    @staticmethod
    def _compute_atm_iv_front(chain: pd.DataFrame, spot: float) -> float:
        """Front-month at-the-money IV.

        Algorithm
        ---------
        1. For each expiry, find the strike closest to spot (the "ATM strike").
        2. Average call and put IV at that strike (skip NaN).
        3. Return the value at the *nearest non-zero-DTE expiry*. If only one
           expiry is loaded, that's the value.

        Falls back gracefully (returns NaN) when the chain is missing required
        columns or has no IV-bearing rows.
        """
        if chain.empty or "iv" not in chain.columns or not np.isfinite(spot):
            return float("nan")
        df = chain.copy()
        df["iv_num"] = pd.to_numeric(df["iv"], errors="coerce")
        df = df[df["iv_num"].notna()]
        if df.empty or "expiration" not in df.columns or "strike" not in df.columns:
            return float("nan")
        df["dist"] = (df["strike"].astype(float) - spot).abs()

        # ATM IV per expiry: avg of call+put at the closest strike
        atm_per_expiry: list[tuple[pd.Timestamp, float]] = []
        for expiry, group in df.groupby("expiration"):
            if group.empty:
                continue
            min_dist = group["dist"].min()
            atm_rows = group[group["dist"] <= min_dist * 1.0001]
            iv = float(atm_rows["iv_num"].mean())
            atm_per_expiry.append((expiry, iv))
        if not atm_per_expiry:
            return float("nan")

        # Sort by expiry date ascending → front month is first
        atm_per_expiry.sort(key=lambda t: t[0])
        return float(atm_per_expiry[0][1])

    def estimate_quote_cost(self) -> None:
        if self.data_source_var.get() != "Databento":
            messagebox.showinfo(
                "Cost estimate",
                f"Cost estimate only applies to Databento. Current source: {self.data_source_var.get()}.",
            )
            return

        def task() -> None:
            cost = estimate_request_cost(
                schema="cmbp-1",
                symbols=[],
                start=self.start_time_var.get(),
                end=self.end_time_var.get() or None,
                underlying=self.underlying_var.get().strip().upper() or "MSTR",
                stype_in="parent",
            )
            text = "Databento did not return an estimate." if cost is None else f"Estimated Databento cost: ${cost:,.4f}"
            self.root.after(0, lambda: messagebox.showinfo("Cost estimate", text))

        threading.Thread(target=task, daemon=True).start()

    @staticmethod
    def _format_cell(col: str, value) -> str:
        """Format a DataFrame cell for display.

        - Greek columns are stored as raw mathematical partial derivatives; apply
          the trader-screen scaling (e.g. theta × 1/365 = $/day) at display time.
        - Per-column decimal places via ``_DECIMALS``; falls back to 4.
        """
        if pd.isna(value):
            return ""
        if isinstance(value, float):
            scaled = value * _TRADER_SCALES.get(col, 1.0)
            return f"{scaled:.{_DECIMALS.get(col, 4)}f}"
        return str(value)


if __name__ == "__main__":
    root = tk.Tk()
    app = MstrOptionsWorkstation(root)
    root.mainloop()
