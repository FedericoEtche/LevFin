"""Databento adapter for OPRA option chains.

Re-exports the existing top-level ``databento_options`` module so the
``mstr_options_lab`` namespace is self-contained. When that module is
eventually migrated under this package, callers in this namespace don't change.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the workspace root is on sys.path so we can import the existing module
_workspace_root = Path(__file__).resolve().parent.parent.parent
if str(_workspace_root) not in sys.path:
    sys.path.insert(0, str(_workspace_root))

from databento_options import (  # noqa: E402,F401
    DatabentoConfig,
    OPRA_DATASET,
    DEFAULT_CACHE_DIR,
    parent_symbol,
    parse_occ_symbol,
    historical_client,
    fetch_option_definitions,
    fetch_cmbp1_snapshot,
    estimate_request_cost,
    enrich_chain_with_quotes,
    sample_mstr_chain,
)
