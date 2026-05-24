# MSTR Options Workstation

This is the first narrow desktop MVP for the options app.

It starts with `MSTR` and Databento OPRA data:

- Parent symbol: `MSTR.OPT`
- Dataset: `OPRA.PILLAR`
- Definitions schema: `definition`
- Quote schema: `cmbp-1`

## Run

Install the basic dependencies if needed:

```powershell
pip install -U pandas pyarrow databento
```

Set your Databento key for real data:

```powershell
$env:DATABENTO_API_KEY = "db-your-key-here"
```

Run the desktop app:

```powershell
python .\mstr_options_workstation.py
```

If no API key is set, the app opens in Sample Mode. Uncheck Sample Mode after setting
`DATABENTO_API_KEY`.

## First workflow

1. Keep `Underlying` as `MSTR`.
2. Enter a realistic spot price.
3. Use a historical quote window that Databento can serve.
4. Click `Estimate Quote Cost` before making a real quote request.
5. Click `Load Chain`.

The table shows option symbol, expiration, right, strike, bid, ask, mid, IV, and Greeks.

## Notes

Databento OPRA historical data uses OCC raw symbols, for example:

```text
MSTR  260116C00500000
```

The app parses these into underlying, expiration, option right, and strike.
