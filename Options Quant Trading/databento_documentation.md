# Databento Python API Documentation: OPRA & US Equities

This document compiles the essential documentation, code snippets, and dataset references needed to interact with the **Databento** Python API for both **Historical** and **Live** data, specifically focusing on **OPRA** (Options) and **US Equities**.

## 1. Installation & Setup

To get started, install the official Databento Python client via pip:

```bash
pip install -U databento
```

**Authentication**: 
Both the Historical and Live clients require a 32-character API key starting with `db-`. The best practice is to set it as an environment variable so the client can automatically pick it up:
```bash
export DATABENTO_API_KEY="db-YOUR_API_KEY_HERE"
```
Alternatively, you can pass it directly into the client initialization as shown in the examples below.

## 2. Dataset Identifiers

When querying the API, you must specify the dataset you want to access. Databento uses specific string identifiers for its datasets:

### US Equities
- `DBEQ.MAX`: **Databento Equities Consolidated** feed. This is a proprietary consolidated feed covering multiple US equity venues.
- `XNAS.ITCH`: **Nasdaq TotalView-ITCH**. The proprietary direct feed from Nasdaq, offering full depth of book.

### OPRA (Options)
- `OPRA.PILLAR`: **OPRA** (Options Price Reporting Authority) feed. Includes consolidated trades and NBBO across all 18 US equity options exchanges.

> [!NOTE]
> **Live Data Licensing**: Access to live data (and specifically OPRA) requires completing licensing questionnaires and activating the subscription via your Databento user portal. 

---

## 3. Historical Data API

The Historical API is used for accessing data older than 24 hours. The interface relies on the `Historical` client and is highly integrated with `pandas`.

### Example: Fetching Historical Data
Use the `timeseries.get_range` method to pull data over a specific time window.

```python
import databento as db

# 1. Initialize the historical client
# If DATABENTO_API_KEY is set in your env, you can omit the key parameter.
client = db.Historical(key="db-YOUR_API_KEY_HERE")

# 2. Request historical trades for a US Equity (Nasdaq ITCH)
print("Fetching US Equities (XNAS.ITCH) trades...")
equities_data = client.timeseries.get_range(
    dataset="XNAS.ITCH",
    symbols=["AAPL", "MSFT"], # Can be a list of symbols, a single string, or "ALL_SYMBOLS"
    schema="trades",
    start="2024-03-01T09:30:00",
    end="2024-03-01T16:00:00"
)

# Convert to pandas DataFrame for easy analysis
df_equities = equities_data.to_df()
print(df_equities.head())

# 3. Request historical NBBO for OPRA
print("Fetching OPRA Options data...")
opra_data = client.timeseries.get_range(
    dataset="OPRA.PILLAR",
    symbols="SPY",            # Symbology handles option root symbols
    schema="mbp-1",           # mbp-1 provides Top of Book (NBBO)
    start="2024-03-01T09:30:00",
    end="2024-03-01T10:00:00"
)

df_opra = opra_data.to_df()
print(df_opra.head())
```

---

## 4. Live Data API

The Live API provides real-time streaming subscriptions and intraday replay (within the last 24 hours) using a socket-based protocol.

### Example: Subscribing to Live Feeds

```python
import databento as db

# 1. Initialize the live client
live_client = db.Live(key="db-YOUR_API_KEY_HERE")

# 2. Subscribe to the Databento Consolidated Equities feed
live_client.subscribe(
    dataset="DBEQ.MAX",
    schema="trades",
    symbols=["NVDA", "TSLA"]
)

# 3. Subscribe to the OPRA feed
live_client.subscribe(
    dataset="OPRA.PILLAR",
    schema="mbp-1",          # Top of book
    symbols="SPX"            # Index options
)

# 4. Start the stream and process incoming messages
# The start() or stream() method blocks and yields messages as they arrive.
print("Starting live stream...")
for record in live_client.stream():
    # Each record is a Databento Record object (e.g., TradeMsg, Mbp1Msg)
    print(record)
```

> [!WARNING]
> Ensure you have active live data licenses for `DBEQ.MAX`, `XNAS.ITCH`, and `OPRA.PILLAR` in your portal, otherwise the subscription call will be rejected.

---

## 5. Supported Schemas

When requesting data, you must provide a `schema`. Databento standardizes data structures across datasets, so the schemas look the same whether you use Historical or Live API, or if you pull Equities vs. Options.

Common schemas include:
- `trades`: Only execution records.
- `mbo`: Market By Order (Full order book depth, tick-by-tick).
- `mbp-1`: Market By Price, Level 1 (Top of book / NBBO and trades).
- `mbp-10`: Market By Price, Level 10 (Order book aggregated by price up to 10 levels deep).
- `ohlcv-1s`: Open, High, Low, Close, Volume aggregated into 1-second bars. (Also available in `1m`, `1h`, `1d`).
- `definition`: Instrument definitions and symbol mappings.

## References
- Official Docs: [https://docs.databento.com/](https://docs.databento.com/)
- Historical API Reference: [https://docs.databento.com/api-reference-historical](https://docs.databento.com/api-reference-historical)
- Live API Reference: [https://docs.databento.com/api-reference-live](https://docs.databento.com/api-reference-live)
