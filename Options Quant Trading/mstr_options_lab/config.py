"""Shared constants and conventions.

Time conventions
----------------
- TRADING_DAYS = 252  : volatility annualization
- CALENDAR_DAYS = 365 : option time-to-expiry (default for pricing)

Two are used because they answer different questions:
- IV is conventionally annualized by sqrt(252) (trading days).
- BSM time-to-expiry T is wall-clock years; conventionally calendar/365.

Pricing & Greek scaling
-----------------------
- Theta returned per year (raw ∂C/∂t). Multiply by 1/365 for per-day display.
- Vega returned per unit vol (raw ∂C/∂σ). Multiply by 0.01 for per-1%-vol.
- Rho returned per unit rate (raw ∂C/∂r). Multiply by 0.01 for per-1%-rate.
- Greeks helpers expose `scale="trader"` to apply these conventions.

.env.local loader
-----------------
On first import, reads project-root ``.env.local`` (if it exists) and populates
``os.environ`` for any keys not already set. Lets the workstation pick up
``DATABENTO_API_KEY`` without depending on whether the parent shell's env
propagates to Python subprocesses (which it doesn't in Claude Code).
"""

import os
from pathlib import Path

TRADING_DAYS = 252
CALENDAR_DAYS = 365

DEFAULT_RATE = 0.045
DEFAULT_DIVIDEND_YIELD = 0.0


def _load_env_file(path: Path) -> int:
    """Minimal .env reader — no python-dotenv dep. Returns count of vars set."""
    if not path.exists():
        return 0
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and val and key not in os.environ:
            os.environ[key] = val
            n += 1
    return n


# Project root is the parent of mstr_options_lab/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
_load_env_file(PROJECT_ROOT / ".env.local")
