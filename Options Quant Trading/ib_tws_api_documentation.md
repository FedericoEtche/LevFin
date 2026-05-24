# IBKR TWS API Documentation: OPRA & US Equities

This document compiles the essential documentation and code snippets needed to interact with the **Interactive Brokers (IBKR) TWS API** for both **Historical** and **Live** data, focusing on **OPRA** (Options) and **US Equities**. 

While Interactive Brokers provides a native `ibapi` library, the Python community standard (and the standard pattern used in your MSTR Wheel Strategy) is `ib_insync`, an asynchronous wrapper that drastically simplifies connection management and data handling.

## 1. Prerequisites & Market Data Subscriptions

Unlike Databento, IBKR requires you to have the **TWS (Trader Workstation)** or **IB Gateway** software running locally to act as the bridge between your code and their servers.

### Required Subscriptions via IBKR Account Management:
- **US Equities**: "US Securities Snapshot and AMEX/NASDAQ/NYSE" (Network A, B, C) for real-time equity data.
- **OPRA**: "OPRA (Options Price Reporting Authority)" for real-time US options data.

> [!IMPORTANT]
> You must enable ActiveX and Socket Clients in TWS settings (API -> Settings) and take note of the **Socket Port** (usually `7496` for live, `7497` for paper trading).

## 2. Installation & Setup

Install the `ib_insync` package via pip:
```bash
pip install ib-insync
```

### Establishing a Connection
```python
from ib_insync import *

# Initialize the IB client
ib = IB()

# Connect to TWS or IB Gateway
# 127.0.0.1 is your localhost. 
# 7497 is the default paper trading port (use 7496 for live).
# clientId must be unique per connected script.
ib.connect('127.0.0.1', 7497, clientId=1)
print(ib.isConnected())
```

## 3. Contract Definition & Qualification

IBKR uses strict contract definitions. Before requesting any data, you must define the contract (Stock or Option) and "qualify" it. Qualifying a contract fetches its unique `conId` (Contract ID) from IBKR's database, ensuring there's no ambiguity.

```python
# Define a US Equity (Stock)
stock = Stock('AAPL', 'SMART', 'USD')

# Define an Option (OPRA)
# SPY Call, Expiry 2024-06-21, 500 Strike
option = Option('SPY', '20240621', 500, 'C', 'SMART')

# Qualify contracts to fill in missing details (conId, exchange routing)
ib.qualifyContracts(stock, option)
```

## 4. Historical Data API (`reqHistoricalData`)

IBKR provides historical data in various bar sizes (1 min, 5 min, 1 day, etc.).

### Example: Fetching Historical Data
```python
# 1. Fetch Historical Data for US Equity
print("Fetching Historical Stock Data...")
stock_bars = ib.reqHistoricalData(
    contract=stock,
    endDateTime='',            # Empty string means 'now'
    durationStr='30 D',        # Duration: '30 D' (30 days), '1 Y' (1 year)
    barSizeSetting='1 day',    # Bar size: '1 min', '1 hour', '1 day'
    whatToShow='TRADES',       # What to show: 'TRADES', 'MIDPOINT', 'BID_ASK'
    useRTH=True                # True to use Regular Trading Hours only
)

# Convert to pandas DataFrame
df_stock = util.df(stock_bars)
print(df_stock.tail())

# 2. Fetch Historical Data for an Option (OPRA)
print("Fetching Historical Option Data...")
option_bars = ib.reqHistoricalData(
    contract=option,
    endDateTime='',
    durationStr='5 D',
    barSizeSetting='5 mins',
    whatToShow='TRADES',
    useRTH=True
)

df_option = util.df(option_bars)
print(df_option.tail())
```

## 5. Live Data API (`reqMktData`)

To stream live data, you request market data for a qualified contract. IBKR streams data back asynchronously. In `ib_insync`, you typically run the IB event loop to process these ticks.

### Market Data Types
IBKR categorizes market data requests:
- `1` : Live Data (requires subscriptions)
- `2` : Frozen Data (last known price after market close)
- `3` : Delayed Data (if you don't have live subscriptions, delayed by 15-20 mins)
- `4` : Delayed-Frozen Data

```python
# Set data type to live (1). If market is closed, switch to frozen (2).
ib.reqMarketDataType(1) 

# 1. Subscribe to Live Stock Data
stock_ticker = ib.reqMktData(stock, '', False, False)

# 2. Subscribe to Live Option Data & Greeks
# genericTickList '106' requests implied volatility and option model Greeks
option_ticker = ib.reqMktData(option, '106', False, False)

# 3. Define a callback function to handle incoming ticks
def onPendingTickers(tickers):
    for t in tickers:
        if t.contract == stock:
            print(f"Live AAPL - Bid: {t.bid}, Ask: {t.ask}, Last: {t.last}")
        elif t.contract == option:
            print(f"Live SPY Option - Last: {t.last}")
            if t.modelGreeks:
                print(f"  Delta: {t.modelGreeks.delta}, IV: {t.modelGreeks.impliedVol}")

# Attach the callback event
ib.pendingTickersEvent += onPendingTickers

# 4. Keep the connection open and listen to the stream
# ib.sleep() processes incoming network events. 
# While this loop runs, onPendingTickers will print live updates.
try:
    print("Starting live stream... Press Ctrl+C to stop.")
    while True:
        ib.sleep(1) # Sleep 1 second, but keep processing events
except KeyboardInterrupt:
    print("Stopping stream.")
finally:
    ib.disconnect()
```

> [!TIP]
> **Options Chain Discovery**: If you don't know the exact option contract details, use `ib.reqContractDetails()` or `ib.reqTickers()` in combination with `ib.reqSecDefOptParams()` to dynamically discover available expirations and strikes for a given underlying asset.

## Summary of Differences (Databento vs IBKR)
1. **Architecture**: Databento uses direct REST/Socket connections to their cloud. IBKR requires a local GUI (TWS/Gateway) acting as an intermediary proxy.
2. **Contract Identifiers**: Databento uses symbology like `AAPL` and `dataset="DBEQ.MAX"`. IBKR uses strongly-typed `Contract` objects that must be mathematically qualified with `conId`.
3. **Data Throttling**: IBKR actively paces and throttles historical requests (e.g., max 60 requests per 10 minutes for certain data types) and limits live ticker subscriptions (~100 concurrent streams by default). Databento has much higher historical throughput.
