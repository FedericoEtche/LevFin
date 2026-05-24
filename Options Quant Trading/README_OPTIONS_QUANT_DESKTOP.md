# Options Quant Workstation

New PyQt6 Windows desktop app for the MSTR-focused options pricing and trading
workflow.

## Run

```powershell
python .\run_options_quant_desktop.py
```

The app opens in Sample mode without external connections.

## Databento

Set the key in your shell before launching:

```powershell
$env:DATABENTO_API_KEY = "db-your-key-here"
python .\run_options_quant_desktop.py
```

Use `Databento Historical` as the source. The first implementation requests
OPRA definitions by parent symbol, picks the closest strikes to spot, requests
`cmbp-1` top-of-book snapshots for those raw OCC symbols, and computes IV,
BSM fair value, advanced Greeks, SVI smile, and the Breeden-Litzenberger
risk-neutral distribution.

## IBKR / TWS

Start TWS or IB Gateway first. For paper TWS the default port is usually `7497`.
For live TWS it is usually `7496`.

1. Enable API socket clients in TWS / Gateway.
2. Launch the app.
3. Click `Connect IBKR`.
4. Select `IBKR Snapshot` and click `Load Chain`.

The IBKR adapter uses `ib_insync` and requests option parameters with
`reqSecDefOptParams`, then snapshots nearby calls and puts. IBKR is treated as a
live broker/quote source, while Databento remains the preferred historical OPRA
source because of IBKR pacing and expired-option limitations.

## App Sections

- `Chain`: option chain, mids, IV, BSM fair value, edge, first/second/third-order Greeks.
- `Smile / Surface`: SVI fit for the selected expiration.
- `Implied Distribution`: Breeden-Litzenberger risk-neutral PDF and CDF from the SVI smile.
- `Strategy Lab`: common spreads/straddles/strangles with scenario P/L.
- `Model Lab`: BSM closed form versus Carr-Madan FFT models.
- `Logs`: task and connector status.

## Notes

- The implied distribution is risk-neutral, not a real-world price forecast.
- Do not hardcode API keys in notebooks or source files.
- The current SVI fit is a useful first pass, not a full production SSVI surface
  with calendar-arbitrage enforcement.
