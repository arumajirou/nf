from __future__ import annotations

from math import erf, sqrt
from typing import Dict

import numpy as np
import pandas as pd


def diebold_mariano(
    e1: pd.Series,
    e2: pd.Series,
    h: int,
    loss: str = "mse",
) -> Dict[str, float]:
    """Compute the Diebold‑Mariano test statistic and a two‑sided p‑value.

    Parameters
    ----------
    e1, e2:
        Forecast errors from model 1 and model 2 respectively. They must
        correspond to the *same* forecast origins.
    h:
        Forecast horizon. Used to approximate the long‑run variance via
        a Newey‑West style estimator with ``h-1`` lags.
    loss:
        Either ``"mse"`` or ``"mae"`` defining the loss differential.
    """
    s1 = e1.dropna().astype(float)
    s2 = e2.dropna().astype(float)
    n = int(min(len(s1), len(s2)))
    if n == 0:
        return {"stat": np.nan, "p_value": np.nan}

    s1 = s1.iloc[-n:]
    s2 = s2.iloc[-n:]

    if loss == "mse":
        d = s1 ** 2 - s2 ** 2
    elif loss == "mae":
        d = np.abs(s1) - np.abs(s2)
    else:
        raise ValueError(f"Unsupported loss type for DM test: {loss}")

    d_mean = float(d.mean())
    d_centered = d - d_mean

    # Long‑run variance using a simple Newey‑West estimator.
    gamma0 = float(np.dot(d_centered, d_centered) / n)
    gamma_sum = gamma0
    for lag in range(1, max(h, 1)):
        cov = float(np.dot(d_centered[lag:], d_centered[:-lag]) / n)
        gamma_sum += 2.0 * cov

    var_d = gamma_sum / max(n, 1)
    if var_d <= 0:
        return {"stat": np.nan, "p_value": np.nan}

    dm_stat = d_mean / np.sqrt(var_d)

    # Two‑sided p‑value using normal approximation.
    z = abs(dm_stat) / sqrt(2.0)
    cdf = 0.5 * (1.0 + erf(z))
    p_two_sided = 2.0 * (1.0 - cdf)

    return {"stat": float(dm_stat), "p_value": float(p_two_sided)}
