"""PyQt6 desktop application for options quant analytics."""

from __future__ import annotations

from datetime import date, timedelta
import traceback
from typing import Any, Callable

import numpy as np
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTabWidget,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from . import analytics


class TaskWorker(QThread):
    finished_ok = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, fn: Callable[[], Any], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._fn = fn

    def run(self) -> None:
        try:
            self.finished_ok.emit(self._fn())
        except Exception:
            self.failed.emit(traceback.format_exc())


class DataFrameModel(QAbstractTableModel):
    def __init__(self, frame: pd.DataFrame | None = None) -> None:
        super().__init__()
        self._frame = frame.copy() if frame is not None else pd.DataFrame()

    def set_frame(self, frame: pd.DataFrame) -> None:
        self.beginResetModel()
        self._frame = frame.copy()
        self.endResetModel()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._frame)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._frame.columns)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        value = self._frame.iat[index.row(), index.column()]
        col = str(self._frame.columns[index.column()])
        if role == Qt.ItemDataRole.DisplayRole:
            return self._format_value(value, col)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col in {"raw_symbol", "right", "model"}:
                return int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            return int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        if role == Qt.ItemDataRole.ForegroundRole:
            if col == "right":
                return QColor("#15803d") if str(value).lower().startswith("call") else QColor("#b91c1c")
            if col == "edge_mid_minus_bsm" and pd.notna(value):
                return QColor("#15803d") if float(value) < 0 else QColor("#b91c1c")
        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return str(self._frame.columns[section]).replace("_", " ")
        return str(section + 1)

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        if self._frame.empty:
            return
        self.layoutAboutToBeChanged.emit()
        col = self._frame.columns[column]
        self._frame = self._frame.sort_values(col, ascending=order == Qt.SortOrder.AscendingOrder)
        self.layoutChanged.emit()

    @staticmethod
    def _format_value(value: Any, col: str) -> str:
        if pd.isna(value):
            return ""
        if isinstance(value, pd.Timestamp):
            return value.date().isoformat()
        if hasattr(value, "isoformat") and col == "expiration":
            return value.isoformat()
        if isinstance(value, (float, np.floating)):
            if col in {"iv", "avg_iv"}:
                return f"{float(value) * 100:.2f}%"
            if abs(float(value)) >= 1000:
                return f"{float(value):,.2f}"
            return f"{float(value):.5g}"
        return str(value)


class PlotCanvas(FigureCanvas):
    def __init__(self, rows: int = 1, cols: int = 1) -> None:
        self.figure = Figure(figsize=(8, 5), tight_layout=True)
        self.axes = self.figure.subplots(rows, cols)
        super().__init__(self.figure)


class OptionsQuantMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Options Quant Workstation")
        self.resize(1540, 920)
        self.chain = pd.DataFrame()
        self.current_smile: analytics.SmileFit | None = None
        self.current_distribution: analytics.DistributionResult | None = None
        self._worker: TaskWorker | None = None
        self._ib_bridge = None

        self.chain_model = DataFrameModel()
        self.model_price_model = DataFrameModel()
        self._build_ui()
        self._apply_style()
        self.log("App ready. Sample mode is available without external connections.")

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)

        self.metric_contracts = QLabel("0")
        self.metric_expiries = QLabel("0")
        self.metric_avg_iv = QLabel("-")
        self.metric_atm = QLabel("-")
        metrics = QHBoxLayout()
        for title, label in (
            ("Contracts", self.metric_contracts),
            ("Expirations", self.metric_expiries),
            ("Average IV", self.metric_avg_iv),
            ("Nearest ATM", self.metric_atm),
        ):
            box = QGroupBox(title)
            lay = QVBoxLayout(box)
            label.setObjectName("metricValue")
            lay.addWidget(label)
            metrics.addWidget(box)
        root_layout.addLayout(metrics)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        root_layout.addWidget(splitter, stretch=1)

        left = QWidget()
        left.setMinimumWidth(340)
        left.setMaximumWidth(430)
        left_layout = QVBoxLayout(left)
        splitter.addWidget(left)

        self.source_combo = QComboBox()
        self.source_combo.addItems(["Sample", "Databento Historical", "IBKR Snapshot"])
        self.underlying_edit = QLineEdit("MSTR")
        self.spot_edit = QLineEdit("450")
        self.rate_edit = QLineEdit("0.045")
        self.dividend_edit = QLineEdit("0.0")
        self.asof_edit = QLineEdit(date.today().isoformat())
        self.definition_date_edit = QLineEdit((date.today() - timedelta(days=2)).isoformat())
        self.quote_start_edit = QLineEdit(f"{date.today() - timedelta(days=2)}T15:30:00-04:00")
        self.quote_end_edit = QLineEdit(f"{date.today() - timedelta(days=2)}T15:35:00-04:00")
        self.max_symbols_edit = QLineEdit("120")

        data_group = QGroupBox("Market Data")
        data_form = QFormLayout(data_group)
        data_form.addRow("Source", self.source_combo)
        data_form.addRow("Underlying", self.underlying_edit)
        data_form.addRow("Spot", self.spot_edit)
        data_form.addRow("Rate", self.rate_edit)
        data_form.addRow("Dividend yield", self.dividend_edit)
        data_form.addRow("As of", self.asof_edit)
        data_form.addRow("Definition date", self.definition_date_edit)
        data_form.addRow("Quote start", self.quote_start_edit)
        data_form.addRow("Quote end", self.quote_end_edit)
        data_form.addRow("Max contracts", self.max_symbols_edit)
        left_layout.addWidget(data_group)

        self.ib_host_edit = QLineEdit("127.0.0.1")
        self.ib_port_edit = QLineEdit("7497")
        self.ib_client_id_edit = QLineEdit("19")
        self.ib_status_label = QLabel("Disconnected")
        self.ib_connect_btn = QPushButton("Connect IBKR")
        self.ib_connect_btn.clicked.connect(self.connect_ibkr)

        ib_group = QGroupBox("IBKR / TWS")
        ib_form = QFormLayout(ib_group)
        ib_form.addRow("Host", self.ib_host_edit)
        ib_form.addRow("Port", self.ib_port_edit)
        ib_form.addRow("Client id", self.ib_client_id_edit)
        ib_form.addRow("Status", self.ib_status_label)
        ib_form.addRow(self.ib_connect_btn)
        left_layout.addWidget(ib_group)

        self.load_chain_btn = QPushButton("Load Chain")
        self.load_chain_btn.clicked.connect(self.load_chain)
        self.fit_smile_action_btn = QPushButton("Fit Smile")
        self.fit_smile_action_btn.clicked.connect(self.fit_selected_smile)
        self.derive_dist_action_btn = QPushButton("Derive Distribution")
        self.derive_dist_action_btn.clicked.connect(self.derive_distribution)

        action_group = QGroupBox("Actions")
        action_layout = QVBoxLayout(action_group)
        action_layout.addWidget(self.load_chain_btn)
        action_layout.addWidget(self.fit_smile_action_btn)
        action_layout.addWidget(self.derive_dist_action_btn)
        left_layout.addWidget(action_group)
        left_layout.addStretch(1)

        self.tabs = QTabWidget()
        splitter.addWidget(self.tabs)
        splitter.setStretchFactor(1, 1)

        self._build_chain_tab()
        self._build_smile_tab()
        self._build_distribution_tab()
        self._build_strategy_tab()
        self._build_models_tab()
        self._build_log_tab()

    def _build_chain_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.chain_table = QTableView()
        self.chain_table.setModel(self.chain_model)
        self.chain_table.setSortingEnabled(True)
        self.chain_table.horizontalHeader().setStretchLastSection(False)
        layout.addWidget(self.chain_table)
        self.tabs.addTab(tab, "Chain")

    def _build_smile_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        controls = QHBoxLayout()
        self.smile_expiry_combo = QComboBox()
        self.fit_smile_tab_btn = QPushButton("Fit Smile")
        self.fit_smile_tab_btn.clicked.connect(self.fit_selected_smile)
        controls.addWidget(QLabel("Expiration"))
        controls.addWidget(self.smile_expiry_combo)
        controls.addWidget(self.fit_smile_tab_btn)
        controls.addStretch(1)
        layout.addLayout(controls)
        self.smile_canvas = PlotCanvas(1, 1)
        layout.addWidget(self.smile_canvas, stretch=1)
        self.tabs.addTab(tab, "Smile / Surface")

    def _build_distribution_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        controls = QHBoxLayout()
        self.dist_expiry_combo = QComboBox()
        self.derive_dist_tab_btn = QPushButton("Derive Distribution")
        self.derive_dist_tab_btn.clicked.connect(self.derive_distribution)
        self.dist_mean_label = QLabel("Mean: -")
        self.dist_mode_label = QLabel("Mode: -")
        self.dist_below_label = QLabel("P(S<T spot): -")
        self.dist_range_label = QLabel("P(80%-120% spot): -")
        controls.addWidget(QLabel("Expiration"))
        controls.addWidget(self.dist_expiry_combo)
        controls.addWidget(self.derive_dist_tab_btn)
        controls.addStretch(1)
        controls.addWidget(self.dist_mean_label)
        controls.addWidget(self.dist_mode_label)
        controls.addWidget(self.dist_below_label)
        controls.addWidget(self.dist_range_label)
        layout.addLayout(controls)
        self.dist_canvas = PlotCanvas(1, 2)
        layout.addWidget(self.dist_canvas, stretch=1)
        self.tabs.addTab(tab, "Implied Distribution")

    def _build_strategy_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        controls = QGridLayout()
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(
            [
                "Long Straddle",
                "Short Straddle",
                "Long Strangle",
                "Short Strangle",
                "Long Call Vertical",
                "Short Call Vertical",
                "Long Put Vertical",
                "Short Put Vertical",
            ]
        )
        self.strategy_strike1_edit = QLineEdit("450")
        self.strategy_strike2_edit = QLineEdit("550")
        self.strategy_dte_edit = QLineEdit("30")
        self.strategy_iv_edit = QLineEdit("0.85")
        self.strategy_contracts_edit = QLineEdit("1")
        self.strategy_spot_moves_edit = QLineEdit("-20,-10,-5,0,5,10,20")
        self.strategy_vol_moves_edit = QLineEdit("-20,-10,0,10,20")
        self.strategy_days_elapsed_edit = QLineEdit("0")
        self.price_strategy_btn = QPushButton("Price Strategy")
        self.price_strategy_btn.clicked.connect(self.price_strategy)
        self.run_scenario_btn = QPushButton("Run Scenario")
        self.run_scenario_btn.clicked.connect(self.run_strategy_scenario)
        self.strategy_value_label = QLabel("Mark: -")
        self.strategy_greeks_label = QLabel("Greeks: -")

        fields = [
            ("Strategy", self.strategy_combo),
            ("Strike 1", self.strategy_strike1_edit),
            ("Strike 2", self.strategy_strike2_edit),
            ("DTE", self.strategy_dte_edit),
            ("IV", self.strategy_iv_edit),
            ("Contracts", self.strategy_contracts_edit),
            ("Spot moves %", self.strategy_spot_moves_edit),
            ("IV moves pts", self.strategy_vol_moves_edit),
            ("Days elapsed", self.strategy_days_elapsed_edit),
        ]
        for idx, (label, widget) in enumerate(fields):
            row, col = divmod(idx, 3)
            controls.addWidget(QLabel(label), row, col * 2)
            controls.addWidget(widget, row, col * 2 + 1)
        controls.addWidget(self.price_strategy_btn, 3, 0, 1, 2)
        controls.addWidget(self.run_scenario_btn, 3, 2, 1, 2)
        controls.addWidget(self.strategy_value_label, 3, 4)
        controls.addWidget(self.strategy_greeks_label, 3, 5)
        layout.addLayout(controls)

        self.strategy_canvas = PlotCanvas(1, 2)
        layout.addWidget(self.strategy_canvas, stretch=1)
        self.tabs.addTab(tab, "Strategy Lab")

    def _build_models_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        controls = QHBoxLayout()
        self.model_right_combo = QComboBox()
        self.model_right_combo.addItems(["call", "put"])
        self.model_strike_edit = QLineEdit("450")
        self.model_dte_edit = QLineEdit("30")
        self.model_iv_edit = QLineEdit("0.85")
        self.model_price_btn = QPushButton("Compare Models")
        self.model_price_btn.clicked.connect(self.compare_models)
        for label, widget in (
            ("Right", self.model_right_combo),
            ("Strike", self.model_strike_edit),
            ("DTE", self.model_dte_edit),
            ("IV", self.model_iv_edit),
        ):
            controls.addWidget(QLabel(label))
            controls.addWidget(widget)
        controls.addWidget(self.model_price_btn)
        controls.addStretch(1)
        layout.addLayout(controls)

        split = QSplitter(Qt.Orientation.Horizontal)
        self.model_price_table = QTableView()
        self.model_price_table.setModel(self.model_price_model)
        split.addWidget(self.model_price_table)
        self.model_canvas = PlotCanvas(1, 1)
        split.addWidget(self.model_canvas)
        split.setStretchFactor(1, 1)
        layout.addWidget(split, stretch=1)
        self.tabs.addTab(tab, "Model Lab")

    def _build_log_tab(self) -> None:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        self.tabs.addTab(tab, "Logs")

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow, QWidget { background: #f6f7f9; color: #111827; font-family: Segoe UI; font-size: 10pt; }
            QGroupBox { border: 1px solid #d1d5db; border-radius: 6px; margin-top: 10px; padding: 8px; background: #ffffff; }
            QGroupBox::title { subcontrol-origin: margin; left: 9px; padding: 0 4px; color: #374151; font-weight: 600; }
            QLineEdit, QComboBox { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 5px; }
            QPushButton { background: #1f6feb; color: white; border: 0; border-radius: 5px; padding: 7px 10px; font-weight: 600; }
            QPushButton:hover { background: #1d4ed8; }
            QPushButton:disabled { background: #9ca3af; }
            QTableView { background: #ffffff; gridline-color: #e5e7eb; selection-background-color: #dbeafe; }
            QHeaderView::section { background: #111827; color: #f9fafb; padding: 6px; border: 0; }
            QTabWidget::pane { border: 1px solid #d1d5db; background: #ffffff; }
            QTabBar::tab { background: #e5e7eb; padding: 8px 12px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #ffffff; font-weight: 600; }
            QLabel#metricValue { font-size: 18pt; font-weight: 700; color: #111827; }
            """
        )

    def load_chain(self) -> None:
        self._set_busy(True)
        source = self.source_combo.currentText()
        self.log(f"Loading chain from {source}...")
        if source == "IBKR Snapshot":
            try:
                underlying = self.underlying_edit.text().strip().upper() or "MSTR"
                spot = self._float(self.spot_edit, "Spot")
                rate = self._float(self.rate_edit, "Rate")
                div = self._float(self.dividend_edit, "Dividend yield")
                as_of = analytics.parse_date(self.asof_edit.text())
                self._set_chain(self._load_ibkr_chain_sync(underlying, spot, rate, div, as_of))
            except Exception as exc:
                self._set_busy(False)
                self._error("IBKR load failed", str(exc))
            return

        def task() -> pd.DataFrame:
            underlying = self.underlying_edit.text().strip().upper() or "MSTR"
            spot = self._float(self.spot_edit, "Spot")
            rate = self._float(self.rate_edit, "Rate")
            div = self._float(self.dividend_edit, "Dividend yield")
            as_of = analytics.parse_date(self.asof_edit.text())
            if source == "Sample":
                return analytics.load_sample_chain(underlying, spot, rate, div, as_of)
            if source == "Databento Historical":
                return analytics.load_databento_chain(
                    underlying=underlying,
                    spot=spot,
                    rate=rate,
                    dividend_yield=div,
                    as_of=as_of,
                    definition_date=self.definition_date_edit.text().strip(),
                    quote_start=self.quote_start_edit.text().strip(),
                    quote_end=self.quote_end_edit.text().strip(),
                    max_symbols=self._int(self.max_symbols_edit, "Max contracts"),
                )
            raise RuntimeError(f"Unsupported source: {source}")

        self._run_task(task, self._set_chain)

    def _load_ibkr_chain_sync(
        self,
        underlying: str,
        spot: float,
        rate: float,
        dividend_yield: float,
        as_of: date,
    ) -> pd.DataFrame:
        if self._ib_bridge is None or not self._ib_bridge.connected:
            raise RuntimeError("Connect IBKR/TWS before loading an IBKR snapshot.")
        exps, strikes, _, _ = self._ib_bridge.option_parameters(underlying)
        raw = self._ib_bridge.option_snapshot_chain(
            underlying,
            spot=spot,
            expirations=exps,
            strikes=strikes,
            max_contracts=self._int(self.max_symbols_edit, "Max contracts"),
        )
        return analytics.normalize_chain(raw, spot, rate, dividend_yield, as_of)

    def _set_chain(self, chain: pd.DataFrame) -> None:
        self.chain = chain
        self.chain_model.set_frame(chain)
        self.chain_table.resizeColumnsToContents()
        self._refresh_expiry_controls()
        summary = analytics.summarize_chain(chain, self._float(self.spot_edit, "Spot"))
        self.metric_contracts.setText(f"{summary.contracts:,}")
        self.metric_expiries.setText(f"{summary.expirations:,}")
        self.metric_avg_iv.setText("-" if summary.avg_iv is None else f"{summary.avg_iv:.1%}")
        self.metric_atm.setText(summary.nearest_atm or "-")
        self.log(f"Loaded {len(chain):,} contracts.")
        self._set_busy(False)

    def _refresh_expiry_controls(self) -> None:
        expiries = [exp.isoformat() for exp in analytics.available_expirations(self.chain)]
        for combo in (self.smile_expiry_combo, self.dist_expiry_combo):
            current = combo.currentText()
            combo.clear()
            combo.addItems(expiries)
            if current in expiries:
                combo.setCurrentText(current)

    def fit_selected_smile(self) -> None:
        if self.chain.empty:
            self._warn("Load a chain first.")
            return
        expiry = self.smile_expiry_combo.currentText() or self.dist_expiry_combo.currentText()
        if not expiry:
            self._warn("Select an expiration.")
            return
        try:
            self.current_smile = analytics.fit_smile(
                self.chain,
                expiry,
                self._float(self.spot_edit, "Spot"),
                self._float(self.rate_edit, "Rate"),
                self._float(self.dividend_edit, "Dividend yield"),
                analytics.parse_date(self.asof_edit.text()),
            )
            self._draw_smile(self.current_smile)
            self.log(f"Fitted SVI smile for {expiry}.")
        except Exception as exc:
            self._error("Smile fit failed", str(exc))

    def _draw_smile(self, smile: analytics.SmileFit) -> None:
        ax = self.smile_canvas.axes
        ax.clear()
        observed = smile.observed
        calls = observed[observed["right"] == "call"]
        puts = observed[observed["right"] == "put"]
        ax.scatter(calls["strike"], calls["iv"] * 100, s=28, label="Calls", color="#15803d")
        ax.scatter(puts["strike"], puts["iv"] * 100, s=28, label="Puts", color="#b91c1c")
        ax.plot(smile.curve["strike"], smile.curve["iv"] * 100, color="#1f6feb", linewidth=2.0, label="SVI fit")
        ax.axvline(smile.forward, color="#6b7280", linestyle="--", linewidth=1.0, label="Forward")
        ax.set_title(f"Implied Vol Smile - {smile.expiration.isoformat()}")
        ax.set_xlabel("Strike")
        ax.set_ylabel("IV (%)")
        ax.grid(True, alpha=0.25)
        ax.legend()
        self.smile_canvas.draw()

    def derive_distribution(self) -> None:
        if self.chain.empty:
            self._warn("Load a chain first.")
            return
        expiry = self.dist_expiry_combo.currentText() or self.smile_expiry_combo.currentText()
        if not expiry:
            self._warn("Select an expiration.")
            return
        try:
            self.current_distribution = analytics.implied_distribution(
                self.chain,
                expiry,
                self._float(self.spot_edit, "Spot"),
                self._float(self.rate_edit, "Rate"),
                self._float(self.dividend_edit, "Dividend yield"),
                analytics.parse_date(self.asof_edit.text()),
            )
            self.current_smile = self.current_distribution.smile
            self._draw_smile(self.current_smile)
            self._draw_distribution(self.current_distribution)
            self.log(f"Derived risk-neutral distribution for {expiry}.")
        except Exception as exc:
            self._error("Distribution failed", str(exc))

    def _draw_distribution(self, result: analytics.DistributionResult) -> None:
        ax_pdf, ax_cdf = self.dist_canvas.axes
        ax_pdf.clear()
        ax_cdf.clear()
        grid = result.grid
        spot = self._float(self.spot_edit, "Spot")
        ax_pdf.plot(grid["strike"], grid["pdf"], color="#1f6feb", linewidth=2)
        ax_pdf.axvline(spot, color="#111827", linestyle="--", linewidth=1)
        ax_pdf.axvline(result.mean, color="#15803d", linestyle=":", linewidth=1.5)
        ax_pdf.set_title("Risk-Neutral PDF")
        ax_pdf.set_xlabel("MSTR Price")
        ax_pdf.set_ylabel("Density")
        ax_pdf.grid(True, alpha=0.25)
        ax_cdf.plot(grid["strike"], grid["cdf"], color="#7c3aed", linewidth=2)
        ax_cdf.axvline(spot, color="#111827", linestyle="--", linewidth=1)
        ax_cdf.set_title("Risk-Neutral CDF")
        ax_cdf.set_xlabel("MSTR Price")
        ax_cdf.set_ylabel("Probability")
        ax_cdf.grid(True, alpha=0.25)
        self.dist_mean_label.setText(f"Mean: {result.mean:,.2f}")
        self.dist_mode_label.setText(f"Mode: {result.mode:,.2f}")
        self.dist_below_label.setText(f"P(<spot): {result.prob_below_spot:.1%}")
        self.dist_range_label.setText(f"P(80%-120%): {result.prob_between_80_120_spot:.1%}")
        self.dist_canvas.draw()

    def price_strategy(self) -> None:
        try:
            _, metrics = analytics.price_strategy(
                self.strategy_combo.currentText(),
                self._float(self.spot_edit, "Spot"),
                self._float(self.strategy_strike1_edit, "Strike 1"),
                self._float(self.strategy_strike2_edit, "Strike 2"),
                self._float(self.strategy_dte_edit, "DTE"),
                self._float(self.rate_edit, "Rate"),
                self._float(self.strategy_iv_edit, "IV"),
                self._int(self.strategy_contracts_edit, "Contracts"),
            )
            self.strategy_value_label.setText(f"Mark: ${metrics.value:,.2f}")
            self.strategy_greeks_label.setText(
                f"Delta {metrics.delta:,.2f} | Gamma {metrics.gamma:,.3f} | "
                f"Vega {metrics.vega:,.2f} | Theta {metrics.theta:,.2f}"
            )
            self.log(f"Priced {self.strategy_combo.currentText()}: ${metrics.value:,.2f}.")
        except Exception as exc:
            self._error("Strategy pricing failed", str(exc))

    def run_strategy_scenario(self) -> None:
        try:
            rows = analytics.strategy_grid(
                self.strategy_combo.currentText(),
                self._float(self.spot_edit, "Spot"),
                self._float(self.strategy_strike1_edit, "Strike 1"),
                self._float(self.strategy_strike2_edit, "Strike 2"),
                self._float(self.strategy_dte_edit, "DTE"),
                self._float(self.rate_edit, "Rate"),
                self._float(self.strategy_iv_edit, "IV"),
                self._int(self.strategy_contracts_edit, "Contracts"),
                analytics.parse_float_list(self.strategy_spot_moves_edit.text()),
                analytics.parse_float_list(self.strategy_vol_moves_edit.text()),
                self._float(self.strategy_days_elapsed_edit, "Days elapsed"),
            )
            self._draw_strategy(rows)
            valid_rows = rows.dropna(subset=["pnl"])
            if not valid_rows.empty:
                best = valid_rows.loc[valid_rows["pnl"].idxmax()]
                worst = valid_rows.loc[valid_rows["pnl"].idxmin()]
                self.log(
                    f"Scenario complete. Best ${best['pnl']:,.2f}; worst ${worst['pnl']:,.2f}."
                )
            else:
                self.log("Scenario complete, but no valid P/L could be calculated.")
        except Exception as exc:
            self._error("Scenario failed", str(exc))

    def _draw_strategy(self, rows: pd.DataFrame) -> None:
        ax_line, ax_heat = self.strategy_canvas.axes
        ax_line.clear()
        ax_heat.clear()
        spot_moves = sorted(rows["spot_move_pct"].unique())
        vol_moves = sorted(rows["iv_move_points"].unique())
        for vol_move in vol_moves:
            part = rows[rows["iv_move_points"] == vol_move].sort_values("spot_move_pct")
            ax_line.plot(part["spot_move_pct"], part["pnl"], marker="o", label=f"IV {vol_move:+g} pts")
        ax_line.axhline(0, color="#111827", linestyle="--", linewidth=1)
        ax_line.set_title("Scenario P/L")
        ax_line.set_xlabel("Spot move (%)")
        ax_line.set_ylabel("P/L ($)")
        ax_line.grid(True, alpha=0.25)
        ax_line.legend()

        matrix = np.array(
            [
                [
                    rows[
                        (rows["iv_move_points"] == vol_move)
                        & (rows["spot_move_pct"] == spot_move)
                    ]["pnl"].iloc[0]
                    for spot_move in spot_moves
                ]
                for vol_move in vol_moves
            ]
        )
        ax_heat.imshow(matrix, aspect="auto", cmap="RdYlGn", origin="lower")
        ax_heat.set_title("P/L Heatmap")
        ax_heat.set_xticks(range(len(spot_moves)))
        ax_heat.set_xticklabels([f"{x:g}" for x in spot_moves])
        ax_heat.set_yticks(range(len(vol_moves)))
        ax_heat.set_yticklabels([f"{x:+g}" for x in vol_moves])
        ax_heat.set_xlabel("Spot move (%)")
        ax_heat.set_ylabel("IV move (pts)")
        self.strategy_canvas.draw()

    def compare_models(self) -> None:
        try:
            prices = analytics.model_price_table(
                spot=self._float(self.spot_edit, "Spot"),
                strike=self._float(self.model_strike_edit, "Strike"),
                days_to_expiry=self._float(self.model_dte_edit, "DTE"),
                rate=self._float(self.rate_edit, "Rate"),
                dividend_yield=self._float(self.dividend_edit, "Dividend yield"),
                vol=self._float(self.model_iv_edit, "IV"),
                right=self.model_right_combo.currentText(),
            )
            self.model_price_model.set_frame(prices)
            self.model_price_table.resizeColumnsToContents()
            ax = self.model_canvas.axes
            ax.clear()
            ax.barh(prices["model"], prices["price"], color="#1f6feb")
            ax.set_title("Model Price Comparison")
            ax.set_xlabel("Option price")
            ax.grid(True, axis="x", alpha=0.25)
            self.model_canvas.draw()
            self.log("Compared model prices.")
        except Exception as exc:
            self._error("Model comparison failed", str(exc))

    def connect_ibkr(self) -> None:
        try:
            from .ibkr_bridge import IbkrBridge, IbkrConnection

            if self._ib_bridge is None:
                self._ib_bridge = IbkrBridge()
            self._ib_bridge.connect(
                IbkrConnection(
                    host=self.ib_host_edit.text().strip(),
                    port=self._int(self.ib_port_edit, "IBKR port"),
                    client_id=self._int(self.ib_client_id_edit, "IBKR client id"),
                )
            )
            self.ib_status_label.setText("Connected")
            self.log("Connected to IBKR/TWS.")
        except Exception as exc:
            self.ib_status_label.setText("Disconnected")
            self._error("IBKR connection failed", str(exc))

    def _run_task(self, fn: Callable[[], Any], on_success: Callable[[Any], None]) -> None:
        self._worker = TaskWorker(fn, self)
        self._worker.finished_ok.connect(on_success)
        self._worker.failed.connect(self._task_failed)
        self._worker.start()

    def _task_failed(self, details: str) -> None:
        self._set_busy(False)
        self.log(details)
        self._error("Task failed", details.splitlines()[-1] if details else "Unknown error")

    def _set_busy(self, busy: bool) -> None:
        for button in (
            self.load_chain_btn,
            self.fit_smile_action_btn,
            self.fit_smile_tab_btn,
            self.derive_dist_action_btn,
            self.derive_dist_tab_btn,
        ):
            button.setDisabled(busy)

    def _float(self, edit: QLineEdit, name: str) -> float:
        try:
            return float(edit.text().strip())
        except ValueError as exc:
            raise ValueError(f"{name} must be numeric.") from exc

    def _int(self, edit: QLineEdit, name: str) -> int:
        try:
            return int(float(edit.text().strip()))
        except ValueError as exc:
            raise ValueError(f"{name} must be an integer.") from exc

    def _warn(self, message: str) -> None:
        QMessageBox.warning(self, "Options Quant Workstation", message)

    def _error(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)

    def log(self, message: str) -> None:
        self.log_text.appendPlainText(message)


def main() -> int:
    app = QApplication([])
    try:
        from ib_insync import util
        util.useQt()
    except ImportError:
        pass  # ib_insync is optional
    window = OptionsQuantMainWindow()
    window.show()
    return app.exec()
