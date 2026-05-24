"""Data adapters.

- ``databento`` — historical OPRA chains via Databento
- ``ibkr`` — live/snapshot chains via Interactive Brokers TWS (ib_insync)

Both adapters return DataFrames with the SAME schema (raw_symbol, underlying,
expiration, right, strike, bid_px_00, ask_px_00, days_to_expiry, ...) so the
workstation can switch sources without other code changes.
"""

from . import databento  # noqa: F401
from . import databento_live  # noqa: F401
from . import ibkr  # noqa: F401
from .ibkr import IBKRClient, IBKRConfig, IB_INSYNC_AVAILABLE  # noqa: F401
from .databento_live import DatabentoLiveClient, DatabentoLiveConfig  # noqa: F401
