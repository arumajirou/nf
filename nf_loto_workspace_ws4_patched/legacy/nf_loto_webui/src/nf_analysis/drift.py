from __future__ import annotations

from typing import Dict, Iterable, Optional

import numpy as np
import pandas as pd


def _histogram_kl(p: np.ndarray, q: np.ndarray, eps: float = 1e-8) -> float:
    """KL divergence between two non‑negative histograms.

    Both histograms are normalised internally; zero bins are smoothed
    with ``eps`` so that division is well‑defined.
    """
    p = p.astype(float) + eps
    q = q.astype(float) + eps
    p /= p.sum()
    q /= q.sum()
    return float(np.sum(p * np.log(p / q)))


def compute_univariate_drift(
    base: pd.Series,
    current: pd.Series,
    n_bins: int = 20,
) -> Dict[str, float]:
    """Compute simple drift metrics for a single numeric variable.

    Metrics:
    - ``mean_diff``: current.mean() - base.mean()
    - ``std_ratio``: current.std() / base.std()
    - ``kl_div``: histogram‑based KL divergence between base and current
    """
    base = base.dropna().astype(float)
    current = current.dropna().astype(float)

    if len(base) == 0 or len(current) == 0:
        return {"mean_diff": np.nan, "std_ratio": np.nan, "kl_div": np.nan}

    mean_diff = float(current.mean() - base.mean())
    base_std = float(base.std(ddof=1) + 1e-8)
    current_std = float(current.std(ddof=1) + 1e-8)
    std_ratio = current_std / base_std

    all_vals = np.concatenate([base.values, current.values])
    # When all values are identical, fall back to a tiny range to avoid NaNs.
    vmin, vmax = float(all_vals.min()), float(all_vals.max())
    if vmin == vmax:
        vmin -= 0.5
        vmax += 0.5
    bins = np.linspace(vmin, vmax, n_bins + 1)

    p_hist, _ = np.histogram(base.values, bins=bins)
    q_hist, _ = np.histogram(current.values, bins=bins)
    kl = _histogram_kl(p_hist, q_hist)

    return {"mean_diff": mean_diff, "std_ratio": std_ratio, "kl_div": kl}


def compute_dataframe_drift(
    base_df: pd.DataFrame,
    current_df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    n_bins: int = 20,
) -> pd.DataFrame:
    """Compute drift metrics for multiple columns at once.

    Parameters
    ----------
    base_df, current_df:
        DataFrames containing at least the columns of interest.
    columns:
        If omitted, the intersection of numeric columns in both frames
        is used.
    """
    if columns is None:
        cols = sorted(
            set(base_df.columns)
            .intersection(current_df.columns)
        )
        # Restrict to numeric columns only
        cols = [c for c in cols if np.issubdtype(base_df[c].dtype, np.number)]
    else:
        cols = list(columns)

    records = []
    for col in cols:
        metrics = compute_univariate_drift(base_df[col], current_df[col], n_bins=n_bins)
        rec = {"column_name": col}
        rec.update(metrics)
        records.append(rec)
    return pd.DataFrame.from_records(records)
