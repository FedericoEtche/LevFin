"""
mstr_options_lab — options pricing & analytics library for MSTR (and any equity).

Public surface (most-used entrypoints):

    from mstr_options_lab.pricing import bs_price, bs_implied_vol
    from mstr_options_lab.pricing.carr_madan import fft_call_prices, fft_price_one
    from mstr_options_lab.pricing.characteristic_fns import (
        bsm_cf, heston_cf, merton_cf, variance_gamma_cf, HestonParams, MertonParams, VGParams,
    )
    from mstr_options_lab.greeks.analytical import bs_greeks
    from mstr_options_lab.greeks.numerical import fd_greeks
    from mstr_options_lab.surface.svi import fit_svi_slice, svi_total_variance
    from mstr_options_lab.implied_dist.breeden_litzenberger import risk_neutral_pdf
"""

from . import config  # noqa: F401
