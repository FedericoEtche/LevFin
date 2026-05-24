import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from datetime import datetime
from options_core import (
    CALENDAR_DAYS,
    OptionLeg,
    normalize_implied_vol,
    rank_and_percentile,
    scenario_table,
    strategy_metrics,
)
import warnings
warnings.filterwarnings('ignore')

class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.connected = False
        self.historical_data = {}
        
    def error(self, reqId, errorCode, errorString):
        # Filter out irrelevant warnings about fractional shares
        if errorCode == 2176 and "fractional share" in errorString.lower():
            return  # Ignore this specific warning
        print(f"Error {errorCode}: {errorString}")
        
    def nextValidId(self, orderId):
        self.connected = True
        print("Connected to IB")
        
    def historicalData(self, reqId, bar):
        if reqId not in self.historical_data:
            self.historical_data[reqId] = []
        self.historical_data[reqId].append({
            'date': bar.date,
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume
        })
        
    def historicalDataEnd(self, reqId, start, end):
        print(f"Historical data received for reqId {reqId}")
    


class ImpliedVolatilityDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Implied Volatility Trading Dashboard")
        self.root.geometry("1400x1200")  # Increased height to accommodate larger text areas
        
        # Data storage
        self.option_data = None
        self.volatility_data = None
        self.current_implied_vol = None
        
        # IB connection
        self.ib_app = IBApp()
        self.connected = False
        
        # Historical IB option-IV bars have ambiguous units across workflows.
        # This legacy dashboard keeps the original decimal-daily assumption explicit.
        self.iv_unit_mode = "decimal_daily"
        self.last_strategy_metrics = None
        self.last_scenario_rows = None
        
        self.setup_ui()
    
    def create_equity_contract(self, symbol):
        """Create an equity contract for the given symbol"""
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Interactive Brokers Connection", padding="5")
        conn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(conn_frame, text="Host:").grid(row=0, column=0, padx=(0, 5))
        self.host_var = tk.StringVar(value="127.0.0.1")
        ttk.Entry(conn_frame, textvariable=self.host_var, width=15).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=2, padx=(0, 5))
        self.port_var = tk.StringVar(value="7497")
        ttk.Entry(conn_frame, textvariable=self.port_var, width=10).grid(row=0, column=3, padx=(0, 10))
        
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect_ib)
        self.connect_btn.grid(row=0, column=4, padx=(0, 10))
        
        self.disconnect_btn = ttk.Button(conn_frame, text="Disconnect", command=self.disconnect_ib, state="disabled")
        self.disconnect_btn.grid(row=0, column=5)
        
        # Data query frame
        data_frame = ttk.LabelFrame(main_frame, text="Data Query", padding="5")
        data_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(data_frame, text="Symbol:").grid(row=0, column=0, padx=(0, 5))
        self.symbol_var = tk.StringVar(value="SPY")
        ttk.Entry(data_frame, textvariable=self.symbol_var, width=10).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(data_frame, text="Duration:").grid(row=0, column=2, padx=(0, 5))
        self.duration_var = tk.StringVar(value="2 Y")
        ttk.Entry(data_frame, textvariable=self.duration_var, width=10).grid(row=0, column=3, padx=(0, 10))

        ttk.Label(data_frame, text="IV Unit:").grid(row=0, column=4, padx=(0, 5))
        self.iv_unit_var = tk.StringVar(value=self.iv_unit_mode)
        iv_unit_combo = ttk.Combobox(
            data_frame,
            textvariable=self.iv_unit_var,
            values=("decimal_daily", "percent_daily", "decimal_annual", "percent_annual", "auto_annual"),
            width=16,
            state="readonly",
        )
        iv_unit_combo.grid(row=0, column=5, padx=(0, 10))
        
        # Remove volatility window control since we're getting IV data
        # ttk.Label(data_frame, text="Vol Window:").grid(row=0, column=4, padx=(0, 5))
        # self.vol_window_var = tk.StringVar(value="20")
        # ttk.Entry(data_frame, textvariable=self.vol_window_var, width=8).grid(row=0, column=5, padx=(0, 10))
        
        self.query_btn = ttk.Button(data_frame, text="Query IV Data", command=self.query_data, state="disabled")
        self.query_btn.grid(row=0, column=6, padx=(0, 10))
        
        self.analyze_btn = ttk.Button(data_frame, text="Analyze Implied Vol", command=self.analyze_volatility, state="disabled")
        self.analyze_btn.grid(row=0, column=7)
        
        # Current Implied Volatility Display frame
        vol_frame = ttk.LabelFrame(main_frame, text="Current Implied Volatility", padding="5")
        vol_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Volatility value display
        ttk.Label(vol_frame, text="Current IV:").grid(row=0, column=0, padx=(0, 5))
        self.current_vol_label = ttk.Label(vol_frame, text="N/A", font=("Arial", 12, "bold"))
        self.current_vol_label.grid(row=0, column=1, padx=(0, 20))
        
        # Volatility computation details
        ttk.Label(vol_frame, text="Computation:").grid(row=0, column=2, padx=(0, 5))
        self.vol_computation_label = ttk.Label(vol_frame, text="No data", font=("Arial", 10))
        self.vol_computation_label.grid(row=0, column=3, padx=(0, 10))
        

        
        # Volatility statistics
        ttk.Label(vol_frame, text="Vol Range:").grid(row=0, column=4, padx=(0, 5))
        self.vol_range_label = ttk.Label(vol_frame, text="N/A", font=("Arial", 10))
        self.vol_range_label.grid(row=0, column=5)
        
        # Volatility Regime frame
        regime_frame = ttk.LabelFrame(main_frame, text="Volatility Regime Analysis", padding="5")
        regime_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(regime_frame, text="Current Regime:").grid(row=0, column=0, padx=(0, 5))
        self.regime_label = ttk.Label(regime_frame, text="N/A", font=("Arial", 11, "bold"))
        self.regime_label.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(regime_frame, text="Percentile:").grid(row=0, column=2, padx=(0, 5))
        self.percentile_label = ttk.Label(regime_frame, text="N/A", font=("Arial", 10))
        self.percentile_label.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(regime_frame, text="Mean Reversion Signal:").grid(row=0, column=4, padx=(0, 5))
        self.reversion_label = ttk.Label(regime_frame, text="N/A", font=("Arial", 10))
        self.reversion_label.grid(row=0, column=5)

        # Strategy and scenario frame
        strategy_frame = ttk.LabelFrame(main_frame, text="Strategy Pricing & Scenario Lab", padding="5")
        strategy_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(strategy_frame, text="Strategy:").grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.strategy_var = tk.StringVar(value="Long Straddle")
        strategy_combo = ttk.Combobox(
            strategy_frame,
            textvariable=self.strategy_var,
            values=(
                "Long Straddle",
                "Short Straddle",
                "Long Strangle",
                "Short Strangle",
                "Long Call Vertical",
                "Short Call Vertical",
                "Long Put Vertical",
                "Short Put Vertical",
            ),
            width=18,
            state="readonly",
        )
        strategy_combo.grid(row=0, column=1, padx=(0, 10), sticky=tk.W)

        ttk.Label(strategy_frame, text="Spot:").grid(row=0, column=2, padx=(0, 5), sticky=tk.W)
        self.strategy_spot_var = tk.StringVar(value="100")
        ttk.Entry(strategy_frame, textvariable=self.strategy_spot_var, width=10).grid(row=0, column=3, padx=(0, 10))

        ttk.Label(strategy_frame, text="Strike 1:").grid(row=0, column=4, padx=(0, 5), sticky=tk.W)
        self.strategy_strike1_var = tk.StringVar(value="100")
        ttk.Entry(strategy_frame, textvariable=self.strategy_strike1_var, width=10).grid(row=0, column=5, padx=(0, 10))

        ttk.Label(strategy_frame, text="Strike 2:").grid(row=0, column=6, padx=(0, 5), sticky=tk.W)
        self.strategy_strike2_var = tk.StringVar(value="105")
        ttk.Entry(strategy_frame, textvariable=self.strategy_strike2_var, width=10).grid(row=0, column=7, padx=(0, 10))

        ttk.Label(strategy_frame, text="DTE:").grid(row=1, column=0, padx=(0, 5), sticky=tk.W)
        self.strategy_dte_var = tk.StringVar(value="30")
        ttk.Entry(strategy_frame, textvariable=self.strategy_dte_var, width=10).grid(row=1, column=1, padx=(0, 10), sticky=tk.W)

        ttk.Label(strategy_frame, text="Rate:").grid(row=1, column=2, padx=(0, 5), sticky=tk.W)
        self.strategy_rate_var = tk.StringVar(value="0.05")
        ttk.Entry(strategy_frame, textvariable=self.strategy_rate_var, width=10).grid(row=1, column=3, padx=(0, 10))

        ttk.Label(strategy_frame, text="IV Override:").grid(row=1, column=4, padx=(0, 5), sticky=tk.W)
        self.strategy_iv_var = tk.StringVar(value="")
        ttk.Entry(strategy_frame, textvariable=self.strategy_iv_var, width=10).grid(row=1, column=5, padx=(0, 10))

        ttk.Label(strategy_frame, text="Contracts:").grid(row=1, column=6, padx=(0, 5), sticky=tk.W)
        self.strategy_contracts_var = tk.StringVar(value="1")
        ttk.Entry(strategy_frame, textvariable=self.strategy_contracts_var, width=10).grid(row=1, column=7, padx=(0, 10))

        ttk.Label(strategy_frame, text="Spot Moves %:").grid(row=2, column=0, padx=(0, 5), sticky=tk.W)
        self.scenario_spot_moves_var = tk.StringVar(value="-10,-5,0,5,10")
        ttk.Entry(strategy_frame, textvariable=self.scenario_spot_moves_var, width=18).grid(row=2, column=1, padx=(0, 10), sticky=tk.W)

        ttk.Label(strategy_frame, text="IV Moves pts:").grid(row=2, column=2, padx=(0, 5), sticky=tk.W)
        self.scenario_iv_moves_var = tk.StringVar(value="-10,0,10")
        ttk.Entry(strategy_frame, textvariable=self.scenario_iv_moves_var, width=18).grid(row=2, column=3, padx=(0, 10))

        ttk.Label(strategy_frame, text="Days Elapsed:").grid(row=2, column=4, padx=(0, 5), sticky=tk.W)
        self.scenario_days_elapsed_var = tk.StringVar(value="0")
        ttk.Entry(strategy_frame, textvariable=self.scenario_days_elapsed_var, width=10).grid(row=2, column=5, padx=(0, 10))

        self.price_strategy_btn = ttk.Button(strategy_frame, text="Price Strategy", command=self.price_strategy)
        self.price_strategy_btn.grid(row=2, column=6, padx=(0, 10), sticky=tk.W)

        self.run_scenario_btn = ttk.Button(strategy_frame, text="Run Scenario", command=self.run_strategy_scenario)
        self.run_scenario_btn.grid(row=2, column=7, sticky=tk.W)

        self.strategy_value_label = ttk.Label(strategy_frame, text="Mark: N/A", font=("Arial", 10, "bold"))
        self.strategy_value_label.grid(row=3, column=0, columnspan=2, padx=(0, 10), sticky=tk.W)

        self.strategy_greeks_label = ttk.Label(strategy_frame, text="Greeks: N/A", font=("Arial", 10))
        self.strategy_greeks_label.grid(row=3, column=2, columnspan=4, padx=(0, 10), sticky=tk.W)

        self.strategy_move_label = ttk.Label(strategy_frame, text="Expected Move: N/A", font=("Arial", 10))
        self.strategy_move_label.grid(row=3, column=6, columnspan=2, sticky=tk.W)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=6, width=80)  # Increased height for better visibility
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)
        
        # Plot frame
        plot_frame = ttk.LabelFrame(main_frame, text="Implied Volatility Analysis Results", padding="5")
        plot_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        
        # Create matplotlib figure with 3 subplots
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(1, 3, figsize=(18, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def connect_ib(self):
        try:
            host = self.host_var.get()
            port = int(self.port_var.get())
            
            self.log_message(f"Connecting to IB at {host}:{port}...")
            
            # Start connection in separate thread
            def connect_thread():
                try:
                    self.ib_app.connect(host, port, 0)
                    self.ib_app.run()
                except Exception as e:
                    self.log_message(f"Connection error: {e}")
                    
            thread = threading.Thread(target=connect_thread, daemon=True)
            thread.start()
            
            # Wait for connection
            for _ in range(50):  # Wait up to 5 seconds
                if self.ib_app.connected:
                    break
                time.sleep(0.1)
                
            if self.ib_app.connected:
                self.connected = True
                self.connect_btn.config(state="disabled")
                self.disconnect_btn.config(state="normal")
                self.query_btn.config(state="normal")
                self.log_message("Successfully connected to Interactive Brokers")
            else:
                self.log_message("Failed to connect to Interactive Brokers")
                
        except Exception as e:
            self.log_message(f"Connection error: {e}")
            
    def disconnect_ib(self):
        try:
            self.ib_app.disconnect()
            self.connected = False
            self.connect_btn.config(state="normal")
            self.disconnect_btn.config(state="disabled")
            self.query_btn.config(state="disabled")
            self.analyze_btn.config(state="disabled")
            
            # Reset volatility display
            self.current_implied_vol = None
            self.update_current_vol_display()
            
            self.log_message("Disconnected from Interactive Brokers")
        except Exception as e:
            self.log_message(f"Disconnect error: {e}")
            
    def query_data(self):
        if not self.connected:
            messagebox.showerror("Error", "Not connected to Interactive Brokers")
            return
            
        symbol = self.symbol_var.get().upper()
        duration = self.duration_var.get()
        self.iv_unit_mode = self.iv_unit_var.get()
        
        # No longer need vol_window for IV data
        # try:
        #     self.vol_window = int(self.vol_window_var.get())
        # except ValueError:
        #     self.vol_window = 20
        #     self.vol_window_var.set("20")
        
        self.log_message(f"Querying implied volatility data for {symbol}...")
        
        # Clear previous data
        self.ib_app.historical_data.clear()
        
        # Request historical implied volatility data
        contract = self.create_equity_contract(symbol)
        
        self.ib_app.reqHistoricalData(
            reqId=1,
            contract=contract,
            endDateTime="",
            durationStr=duration,
            barSizeSetting="1 day",
            whatToShow="OPTION_IMPLIED_VOLATILITY",  # Changed to get IV data
            useRTH=1,
            formatDate=1,
            keepUpToDate=False,
            chartOptions=[]
        )
        
        # Wait for data with timeout
        timeout = 15  # 15 seconds timeout
        start_time = time.time()
        
        # Wait for historical data
        while 1 not in self.ib_app.historical_data and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        # Process historical implied volatility data
        if 1 in self.ib_app.historical_data:
            data = self.ib_app.historical_data[1]
            if len(data) > 0:
                self.equity_data = pd.DataFrame(data)
                self.equity_data['date'] = pd.to_datetime(self.equity_data['date'])
                self.equity_data.set_index('date', inplace=True)
                
                # Rename 'close' column to 'implied_vol' since that's what we're getting
                self.equity_data['implied_vol'] = self.equity_data['close']
                
                self.log_message(f"Received {len(self.equity_data)} implied volatility data points for {symbol}")
                self.log_message(f"Date range: {self.equity_data.index.min()} to {self.equity_data.index.max()}")
                self.log_message(f"NOTE: Historical IV unit mode is {self.iv_unit_mode}")
                
                # Process implied volatility data
                self.process_implied_volatility()
                
                # Enable analysis
                self.analyze_btn.config(state="normal")
            else:
                self.log_message("No implied volatility data received")
                self.equity_data = None
        else:
            self.log_message("No implied volatility data received - this may not be available for all symbols")
            self.equity_data = None
    
    def process_implied_volatility(self):
        """Process implied volatility data"""
        if self.equity_data is None:
            return
            
        self.log_message("Processing implied volatility data...")
        self.log_message(f"Normalizing IV with unit mode: {self.iv_unit_mode}")
        
        # The 'close' field contains the raw historical IV observation.
        self.equity_data['implied_vol'] = self.equity_data['close'].apply(
            lambda raw: normalize_implied_vol(raw, self.iv_unit_mode)
        )
        
        # Calculate IV percentiles for regime analysis
        
        # Calculate IV percentiles
        self.equity_data['iv_percentile'] = self.equity_data['implied_vol'].rolling(window=252).rank(pct=True)
        
        # Store current implied volatility
        self.current_implied_vol = self.equity_data['implied_vol'].iloc[-1] if len(self.equity_data) > 0 else None
        
        # Create volatility data for analysis
        self.volatility_data = self.equity_data[['implied_vol', 'iv_percentile']].copy()
        
        # Update display
        self.update_current_vol_display()
        
        if self.current_implied_vol is not None:
            self.log_message(f"Current implied volatility: {self.current_implied_vol:.4f} ({self.current_implied_vol*100:.2f}%)")
            self.log_message(f"IV range: {self.equity_data['implied_vol'].min():.4f} - {self.equity_data['implied_vol'].max():.4f}")
        else:
            self.log_message("Failed to process implied volatility data")
    
    def update_current_vol_display(self):
        """Update the current volatility display"""
        if self.current_implied_vol is not None:
            # Update current volatility value
            self.current_vol_label.config(text=f"{self.current_implied_vol:.4f} ({self.current_implied_vol*100:.2f}%)")
            
            # Update computation details
            computation_text = f"Unit mode: {self.iv_unit_mode}"
            self.vol_computation_label.config(text=computation_text)
            
            # Update volatility range
            if self.equity_data is not None:
                vol_min = self.equity_data['implied_vol'].min()
                vol_max = self.equity_data['implied_vol'].max()
                vol_mean = self.equity_data['implied_vol'].mean()
                range_text = f"Min: {vol_min:.3f} | Mean: {vol_mean:.3f} | Max: {vol_max:.3f}"
            else:
                range_text = "N/A"
            
            self.vol_range_label.config(text=range_text)
            
            # Color code based on volatility level
            if self.current_implied_vol > 0.4:  # High volatility (>40%)
                self.current_vol_label.config(foreground="red")
            elif self.current_implied_vol < 0.15:  # Low volatility (<15%)
                self.current_vol_label.config(foreground="green")
            else:  # Normal volatility
                self.current_vol_label.config(foreground="black")
            
            # Update regime analysis
            self.update_regime_analysis()
            

        else:
            self.current_vol_label.config(text="N/A", foreground="black")
            self.vol_computation_label.config(text="No data")
            self.vol_range_label.config(text="N/A")
            self.regime_label.config(text="N/A")
            self.percentile_label.config(text="N/A")
            self.reversion_label.config(text="N/A")
    
    def update_regime_analysis(self):
        """Update volatility regime analysis"""
        if self.volatility_data is None or self.current_implied_vol is None:
            return
            
        # Get current percentile
        current_percentile = self.volatility_data['iv_percentile'].iloc[-1]
        if pd.isna(current_percentile):
            _, current_percentile = rank_and_percentile(
                self.current_implied_vol,
                self.volatility_data['implied_vol'].dropna().tolist()
            )
        if current_percentile is None:
            current_percentile = 0.5
        
        # Determine regime
        if current_percentile > 0.8:
            regime = "HIGH VOLATILITY"
            regime_color = "red"
        elif current_percentile > 0.6:
            regime = "ABOVE AVERAGE"
            regime_color = "orange"
        elif current_percentile > 0.4:
            regime = "NORMAL"
            regime_color = "black"
        elif current_percentile > 0.2:
            regime = "BELOW AVERAGE"
            regime_color = "blue"
        else:
            regime = "LOW VOLATILITY"
            regime_color = "green"
        
        self.regime_label.config(text=regime, foreground=regime_color)
        self.percentile_label.config(text=f"{current_percentile:.1%}")
        
        # Mean reversion signal
        if current_percentile > 0.8:
            reversion = "EXPECT MEAN REVERSION DOWN"
            reversion_color = "blue"
        elif current_percentile < 0.2:
            reversion = "EXPECT MEAN REVERSION UP"
            reversion_color = "red"
        else:
            reversion = "NEUTRAL"
            reversion_color = "black"
        
        self.reversion_label.config(text=reversion, foreground=reversion_color)
    

    def parse_float_input(self, value, name, positive=False, non_negative=False):
        """Parse a numeric UI input with consistent validation."""
        try:
            parsed = float(str(value).strip())
        except ValueError:
            raise ValueError(f"{name} must be a number")

        if not np.isfinite(parsed):
            raise ValueError(f"{name} must be finite")
        if positive and parsed <= 0:
            raise ValueError(f"{name} must be positive")
        if non_negative and parsed < 0:
            raise ValueError(f"{name} must be non-negative")
        return parsed

    def parse_float_list(self, value, name):
        """Parse comma-separated scenario values."""
        parts = [part.strip() for part in str(value).split(",") if part.strip()]
        if not parts:
            raise ValueError(f"{name} must contain at least one value")
        return [self.parse_float_input(part, name) for part in parts]

    def get_strategy_iv(self):
        """Use manual annual IV when supplied; otherwise use the latest normalized IV."""
        manual_iv = self.strategy_iv_var.get().strip()
        if manual_iv:
            raw_iv = self.parse_float_input(manual_iv, "IV Override", non_negative=True)
            return normalize_implied_vol(raw_iv, "auto_annual")

        if self.current_implied_vol is None:
            raise ValueError("Enter IV Override or query IV data first")
        return self.current_implied_vol

    def build_strategy_legs(self):
        """Build option legs from the strategy controls."""
        strategy = self.strategy_var.get()
        strike1 = self.parse_float_input(self.strategy_strike1_var.get(), "Strike 1", positive=True)
        strike2 = self.parse_float_input(self.strategy_strike2_var.get(), "Strike 2", positive=True)
        contracts = int(self.parse_float_input(self.strategy_contracts_var.get(), "Contracts", positive=True))

        low_strike = min(strike1, strike2)
        high_strike = max(strike1, strike2)
        if strategy not in ("Long Straddle", "Short Straddle") and low_strike == high_strike:
            raise ValueError("Strike 1 and Strike 2 must differ for spreads and strangles")

        if strategy == "Long Straddle":
            return [
                OptionLeg("call", strike1, contracts),
                OptionLeg("put", strike1, contracts),
            ]
        if strategy == "Short Straddle":
            return [
                OptionLeg("call", strike1, -contracts),
                OptionLeg("put", strike1, -contracts),
            ]
        if strategy == "Long Strangle":
            return [
                OptionLeg("put", low_strike, contracts),
                OptionLeg("call", high_strike, contracts),
            ]
        if strategy == "Short Strangle":
            return [
                OptionLeg("put", low_strike, -contracts),
                OptionLeg("call", high_strike, -contracts),
            ]
        if strategy == "Long Call Vertical":
            return [
                OptionLeg("call", low_strike, contracts),
                OptionLeg("call", high_strike, -contracts),
            ]
        if strategy == "Short Call Vertical":
            return [
                OptionLeg("call", low_strike, -contracts),
                OptionLeg("call", high_strike, contracts),
            ]
        if strategy == "Long Put Vertical":
            return [
                OptionLeg("put", high_strike, contracts),
                OptionLeg("put", low_strike, -contracts),
            ]
        if strategy == "Short Put Vertical":
            return [
                OptionLeg("put", high_strike, -contracts),
                OptionLeg("put", low_strike, contracts),
            ]

        raise ValueError(f"Unsupported strategy: {strategy}")

    def read_strategy_inputs(self):
        """Read and validate pricing controls."""
        spot = self.parse_float_input(self.strategy_spot_var.get(), "Spot", positive=True)
        days_to_expiry = self.parse_float_input(self.strategy_dte_var.get(), "DTE", non_negative=True)
        rate = self.parse_float_input(self.strategy_rate_var.get(), "Rate")
        vol = self.get_strategy_iv()
        legs = self.build_strategy_legs()
        return spot, days_to_expiry, rate, vol, legs

    def update_strategy_labels(self, metrics, spot, days_to_expiry, vol):
        expected_move = spot * vol * np.sqrt(max(days_to_expiry, 0.0) / CALENDAR_DAYS)

        iv_rank = iv_percentile = None
        if self.volatility_data is not None:
            iv_rank, iv_percentile = rank_and_percentile(
                vol,
                self.volatility_data['implied_vol'].dropna().tolist()
            )

        rank_text = "N/A" if iv_rank is None else f"{iv_rank:.1%}"
        pct_text = "N/A" if iv_percentile is None else f"{iv_percentile:.1%}"

        self.strategy_value_label.config(text=f"Mark: ${metrics.value:,.2f}")
        self.strategy_greeks_label.config(
            text=(
                f"Delta {metrics.delta:.2f} | Gamma {metrics.gamma:.3f} | "
                f"Vega {metrics.vega:.2f} | Theta {metrics.theta:.2f}"
            )
        )
        self.strategy_move_label.config(
            text=f"1sd Move: +/-${expected_move:.2f} | IV Rank {rank_text} | Pctl {pct_text}"
        )

    def price_strategy(self):
        """Price the selected options strategy using the normalized IV input."""
        try:
            spot, days_to_expiry, rate, vol, legs = self.read_strategy_inputs()
            metrics = strategy_metrics(
                legs=legs,
                spot=spot,
                days_to_expiry=days_to_expiry,
                rate=rate,
                vol=vol,
            )
        except ValueError as exc:
            messagebox.showerror("Strategy Input Error", str(exc))
            return None

        self.last_strategy_metrics = metrics
        self.update_strategy_labels(metrics, spot, days_to_expiry, vol)

        legs_text = ", ".join(
            f"{leg.quantity:+d} {leg.right.upper()} {leg.strike:g}" for leg in legs
        )
        self.log_message(f"Priced {self.strategy_var.get()}: {legs_text}")
        self.log_message(
            f"  Spot ${spot:.2f}, DTE {days_to_expiry:.0f}, IV {vol:.1%}, mark ${metrics.value:,.2f}"
        )
        self.log_message(
            f"  Greeks: delta {metrics.delta:.2f}, gamma {metrics.gamma:.3f}, "
            f"vega {metrics.vega:.2f}, theta {metrics.theta:.2f}"
        )
        return spot, days_to_expiry, rate, vol, legs, metrics

    def run_strategy_scenario(self):
        """Run scenario analysis and draw it in the existing plot area."""
        priced = self.price_strategy()
        if priced is None:
            return

        spot, days_to_expiry, rate, vol, legs, metrics = priced
        try:
            spot_moves = self.parse_float_list(self.scenario_spot_moves_var.get(), "Spot Moves")
            iv_moves = self.parse_float_list(self.scenario_iv_moves_var.get(), "IV Moves")
            days_elapsed = self.parse_float_input(
                self.scenario_days_elapsed_var.get(),
                "Days Elapsed",
                non_negative=True,
            )
        except ValueError as exc:
            messagebox.showerror("Scenario Input Error", str(exc))
            return

        rows = scenario_table(
            legs=legs,
            spot=spot,
            days_to_expiry=days_to_expiry,
            rate=rate,
            vol=vol,
            spot_moves_pct=spot_moves,
            vol_moves_points=iv_moves,
            days_elapsed=days_elapsed,
        )
        self.last_scenario_rows = rows
        self.draw_strategy_scenario(rows, spot_moves, iv_moves)

        best = max(rows, key=lambda row: row["pnl"])
        worst = min(rows, key=lambda row: row["pnl"])
        base_candidates = [
            row for row in rows
            if abs(row["spot_move_pct"]) < 1e-9 and abs(row["iv_move_points"]) < 1e-9
        ]
        base = base_candidates[0] if base_candidates else min(
            rows,
            key=lambda row: abs(row["spot_move_pct"]) + abs(row["iv_move_points"])
        )

        self.log_message("Scenario analysis complete")
        self.log_message(
            f"  Base scenario P/L: ${base['pnl']:,.2f} at spot ${base['spot']:.2f}, IV {base['iv']:.1%}"
        )
        self.log_message(
            f"  Best: ${best['pnl']:,.2f} ({best['spot_move_pct']:+.1f}% spot, {best['iv_move_points']:+.1f} vol pts)"
        )
        self.log_message(
            f"  Worst: ${worst['pnl']:,.2f} ({worst['spot_move_pct']:+.1f}% spot, {worst['iv_move_points']:+.1f} vol pts)"
        )

    def draw_strategy_scenario(self, rows, spot_moves, iv_moves):
        """Render scenario output into the original three-panel chart area."""
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        sorted_spot_moves = sorted(spot_moves)
        sorted_iv_moves = sorted(iv_moves)
        row_map = {
            (round(row["iv_move_points"], 8), round(row["spot_move_pct"], 8)): row
            for row in rows
        }

        for iv_move in sorted_iv_moves:
            line_rows = [
                row_map[(round(iv_move, 8), round(spot_move, 8))]
                for spot_move in sorted_spot_moves
            ]
            self.ax1.plot(
                sorted_spot_moves,
                [row["pnl"] for row in line_rows],
                marker="o",
                label=f"IV {iv_move:+.0f} pts",
            )
        self.ax1.axhline(y=0, color="black", linestyle="--", linewidth=1)
        self.ax1.set_xlabel("Spot Move (%)")
        self.ax1.set_ylabel("P/L ($)")
        self.ax1.set_title("Scenario P/L by Spot Move")
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)

        pnl_matrix = np.array([
            [
                row_map[(round(iv_move, 8), round(spot_move, 8))]["pnl"]
                for spot_move in sorted_spot_moves
            ]
            for iv_move in sorted_iv_moves
        ])
        self.ax2.imshow(pnl_matrix, aspect="auto", cmap="RdYlGn", origin="lower")
        self.ax2.set_xticks(range(len(sorted_spot_moves)))
        self.ax2.set_xticklabels([f"{move:g}" for move in sorted_spot_moves])
        self.ax2.set_yticks(range(len(sorted_iv_moves)))
        self.ax2.set_yticklabels([f"{move:+g}" for move in sorted_iv_moves])
        self.ax2.set_xlabel("Spot Move (%)")
        self.ax2.set_ylabel("IV Move (vol pts)")
        self.ax2.set_title("Scenario P/L Heatmap")

        threshold = max(abs(float(np.nanmin(pnl_matrix))), abs(float(np.nanmax(pnl_matrix))), 1.0)
        for row_idx, iv_move in enumerate(sorted_iv_moves):
            for col_idx, spot_move in enumerate(sorted_spot_moves):
                pnl = pnl_matrix[row_idx, col_idx]
                text_color = "white" if abs(pnl) > 0.55 * threshold else "black"
                self.ax2.text(
                    col_idx,
                    row_idx,
                    f"{pnl:,.0f}",
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=8,
                )

        base_iv_move = min(sorted_iv_moves, key=lambda move: abs(move))
        base_rows = [
            row_map[(round(base_iv_move, 8), round(spot_move, 8))]
            for spot_move in sorted_spot_moves
        ]
        self.ax3.plot(
            [row["spot"] for row in base_rows],
            [row["value"] for row in base_rows],
            marker="o",
            color="purple",
            label=f"IV {base_iv_move:+.0f} pts",
        )
        self.ax3.set_xlabel("Underlying Price")
        self.ax3.set_ylabel("Strategy Mark ($)")
        self.ax3.set_title("Strategy Value Across Spot")
        self.ax3.legend()
        self.ax3.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

        
    def analyze_volatility(self):
        if self.equity_data is None or self.volatility_data is None:
            messagebox.showerror("Error", "No data available for analysis")
            return
            
        self.log_message("Analyzing implied volatility patterns...")
        
        # Calculate forward volatility for analysis
        # This calculates the 30-day forward implied volatility by:
        # 1. Taking a 30-day rolling mean of implied vol (smooths the data)
        # 2. Shifting it back 30 days (shift(-30) means looking forward 30 days)
        # WARNING: The shift(-30) means we're looking into the future, which will create NaN values
        # for the last 30 days of our dataset. This is expected and handled by dropna() later.
        # For regression analysis this gives us (current_vol, future_vol) pairs to analyze the relationship.
        vol_forward_30d = self.volatility_data['implied_vol'].rolling(window=30, min_periods=1).mean().shift(-30)
        
        # Create analysis DataFrame
        analysis_df = pd.DataFrame({
            'current_vol': self.volatility_data['implied_vol'],
            'forward_30d_vol': vol_forward_30d,
            'vol_diff': vol_forward_30d - self.volatility_data['implied_vol'],
            'vol_percentile': self.volatility_data['iv_percentile']
        })
        
        # Remove NaN values
        analysis_df = analysis_df.dropna()
        
        if len(analysis_df) < 30:
            self.log_message("Insufficient data for analysis")
            return
            
        # Perform regressions
        from scipy import stats
        
        # Regression 1: Forward Vol on Current Vol
        slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(
            analysis_df['current_vol'], analysis_df['forward_30d_vol']
        )
        
        # Regression 2: Vol Difference on Current Vol
        slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(
            analysis_df['current_vol'], analysis_df['vol_diff']
        )
        
        # Find regime split point (where forward vol = current vol)
        if slope1 != 1:
            intersection_x = intercept1 / (1 - slope1)
        else:
            intersection_x = analysis_df['current_vol'].median()
        
        # Split data into regimes
        high_vol_regime = analysis_df['current_vol'] > intersection_x
        low_vol_regime = analysis_df['current_vol'] <= intersection_x
        
        # Regime-specific regressions
        if high_vol_regime.sum() > 10:
            slope_high, intercept_high, r_high, p_high, std_err_high = stats.linregress(
                analysis_df.loc[high_vol_regime, 'current_vol'],
                analysis_df.loc[high_vol_regime, 'vol_diff']
            )
        else:
            slope_high = intercept_high = r_high = p_high = std_err_high = None
            
        if low_vol_regime.sum() > 10:
            slope_low, intercept_low, r_low, p_low, std_err_low = stats.linregress(
                analysis_df.loc[low_vol_regime, 'current_vol'],
                analysis_df.loc[low_vol_regime, 'vol_diff']
            )
        else:
            slope_low = intercept_low = r_low = p_low = std_err_low = None
        
        # Create plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        # Plot 1: Forward Vol vs Current Vol
        self.ax1.scatter(analysis_df['current_vol'], analysis_df['forward_30d_vol'], alpha=0.6, s=20)
        
        # Add regression line
        x_range = np.linspace(analysis_df['current_vol'].min(), analysis_df['current_vol'].max(), 100)
        y_pred1 = slope1 * x_range + intercept1
        self.ax1.plot(x_range, y_pred1, 'r-', linewidth=2, label=f'Regression R² = {r_value1**2:.3f}')
        
        # Add y=x reference line
        min_val = min(analysis_df['current_vol'].min(), analysis_df['forward_30d_vol'].min())
        max_val = max(analysis_df['current_vol'].max(), analysis_df['forward_30d_vol'].max())
        self.ax1.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=1, alpha=0.7, label='y=x (No Change)')
        
        self.ax1.set_xlabel('Current Implied Volatility')
        self.ax1.set_ylabel('30-Day Forward Average Vol')
        self.ax1.set_title(f'Forward Vol vs Current Vol\ny={slope1:.3f}x+{intercept1:.3f}, R²={r_value1**2:.3f}')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)
        
        # Plot 2: Vol Difference vs Current Vol with regime analysis
        self.ax2.scatter(analysis_df.loc[high_vol_regime, 'current_vol'], 
                        analysis_df.loc[high_vol_regime, 'vol_diff'], 
                        alpha=0.6, s=20, color='red', label='High Vol Regime')
        self.ax2.scatter(analysis_df.loc[low_vol_regime, 'current_vol'], 
                        analysis_df.loc[low_vol_regime, 'vol_diff'], 
                        alpha=0.6, s=20, color='blue', label='Low Vol Regime')
        
        # Add regime-specific regression lines
        if slope_high is not None:
            x_high = analysis_df.loc[high_vol_regime, 'current_vol']
            if len(x_high) > 0:
                x_range_high = np.linspace(x_high.min(), x_high.max(), 100)
                y_pred_high = slope_high * x_range_high + intercept_high
                self.ax2.plot(x_range_high, y_pred_high, 'r-', linewidth=2, 
                             label=f'High Vol R² = {r_high**2:.3f}')
        
        if slope_low is not None:
            x_low = analysis_df.loc[low_vol_regime, 'current_vol']
            if len(x_low) > 0:
                x_range_low = np.linspace(x_low.min(), x_low.max(), 100)
                y_pred_low = slope_low * x_range_low + intercept_low
                self.ax2.plot(x_range_low, y_pred_low, 'b-', linewidth=2, 
                             label=f'Low Vol R² = {r_low**2:.3f}')
        
        # Add zero reference line
        self.ax2.axhline(y=0, color='k', linestyle='--', linewidth=1, alpha=0.7, label='No Change (y=0)')
        
        # Add vertical line at intersection point
        self.ax2.axvline(x=intersection_x, color='g', linestyle=':', linewidth=1, alpha=0.7, 
                        label=f'Regime Split (Vol={intersection_x:.3f})')
        
        self.ax2.set_xlabel('Current Implied Volatility')
        self.ax2.set_ylabel('Vol Difference (Forward - Current)')
        self.ax2.set_title('Vol Difference vs Current Vol (Regime Analysis)')
        self.ax2.legend()
        self.ax2.grid(True, alpha=0.3)
        
        # Plot 3: Volatility Time Series with Regimes
        self.ax3.plot(self.volatility_data.index, self.volatility_data['implied_vol'], 
                     label='Implied Volatility', linewidth=1)
        
        # Add regime bands
        vol_75th = self.volatility_data['implied_vol'].quantile(0.75)
        vol_25th = self.volatility_data['implied_vol'].quantile(0.25)
        
        self.ax3.axhline(y=vol_75th, color='red', linestyle='--', alpha=0.7, label='75th Percentile')
        self.ax3.axhline(y=vol_25th, color='green', linestyle='--', alpha=0.7, label='25th Percentile')
        self.ax3.axhline(y=self.volatility_data['implied_vol'].mean(), color='black', linestyle='-', alpha=0.7, label='Mean')
        
        # Highlight current point
        if self.current_implied_vol is not None:
            self.ax3.scatter(self.volatility_data.index[-1], self.current_implied_vol, 
                           color='red', s=100, zorder=5, label='Current')
        
        self.ax3.set_xlabel('Date')
        self.ax3.set_ylabel('Implied Volatility')
        self.ax3.set_title('Implied Volatility Time Series with Regime Bands')
        self.ax3.legend()
        self.ax3.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        self.ax3.tick_params(axis='x', rotation=45)
        
        # Update canvas
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Log results
        self.log_message(f"Regression 1 - Forward Vol on Current Vol:")
        self.log_message(f"  Slope: {slope1:.4f}, Intercept: {intercept1:.4f}")
        self.log_message(f"  R²: {r_value1**2:.4f}, P-value: {p_value1:.4f}")
        self.log_message(f"  Intersection with y=x at Vol = {intersection_x:.4f}")
        
        self.log_message(f"Regression 2 - Vol Difference on Current Vol:")
        self.log_message(f"  Slope: {slope2:.4f}, Intercept: {intercept2:.4f}")
        self.log_message(f"  R²: {r_value2**2:.4f}, P-value: {p_value2:.4f}")
        
        self.log_message(f"Regime Analysis:")
        if slope_high is not None:
            self.log_message(f"  HIGH VOL regime (Vol > {intersection_x:.3f}):")
            self.log_message(f"    Slope: {slope_high:.4f}, Intercept: {intercept_high:.4f}")
            self.log_message(f"    R²: {r_high**2:.4f}, P-value: {p_high:.4f}")
            self.log_message(f"    Data points: {high_vol_regime.sum()}")
        else:
            self.log_message(f"  HIGH VOL regime: Insufficient data for regression")
            
        if slope_low is not None:
            self.log_message(f"  LOW VOL regime (Vol ≤ {intersection_x:.3f}):")
            self.log_message(f"    Slope: {slope_low:.4f}, Intercept: {intercept_low:.4f}")
            self.log_message(f"    R²: {r_low**2:.4f}, P-value: {p_low:.4f}")
            self.log_message(f"    Data points: {low_vol_regime.sum()}")
        else:
            self.log_message(f"  LOW VOL regime: Insufficient data for regression")
        
        # Trading insights
        if slope1 < 1:
            self.log_message("INSIGHT: Forward volatility tends to mean-revert (slope < 1)")
        else:
            self.log_message("INSIGHT: Forward volatility tends to trend (slope > 1)")
            
        if slope2 < 0:
            self.log_message("INSIGHT: High current volatility predicts lower future volatility (mean reversion)")
        else:
            self.log_message("INSIGHT: High current volatility predicts higher future volatility (momentum)")

def main():
    root = tk.Tk()
    app = ImpliedVolatilityDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
