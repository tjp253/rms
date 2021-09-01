"""
Very simple module to calculate Root-Mean-Square values.
"""

import numpy as np


def combine(x, n=2, period=1, mean=True, noise=False):
    """ Combine several values, using a power of 'n' """
    if not hasattr(x, '__iter__'):  # Single value sent to function
        return x

    x = np.asarray(x)  # convert to numpy array for easier handling

    if noise:
        x = 10 ** (x / 20)  # convert from dB to SPL

    x = x ** n  # SQUARE

    period = np.asarray(period)
    if 1 < period.size < x.size:
        raise ValueError(
                'If more than one period is entered, lengths must match.')
    x = x * period  # Account for time. Used when sample intervals differ.

    nans = np.isnan(x)
    if nans.all():
        return np.nan

    x = np.nansum(x, axis=0)  # SUM

    if mean:  # MEAN
        if period.size == 1:
            divider = np.nansum(~nans, axis=0) * period
        else:
            divider = np.nansum(period, axis=0)

        x /= divider

    x = x ** (1 / n)  # ROOT

    if noise:
        return 20 * np.log10(x)  # convert back to dB
    return x


def rms(x, period=1, noise=False):
    """ Calculate the Root-Mean-Square of 'x' """
    return combine(x, n=2, period=period, noise=noise)
