from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd


def detect_zscore_anomalies(
    residuals: pd.Series,
    threshold: float = 3.0,
) -> Dict[str, List[int]]:
    """Detect anomalies where |z‑score| exceeds ``threshold``.

    Returns a dictionary with one key ``indices`` containing the
    *positional indices* of anomalies (0‑based).
    """
    res = residuals.dropna().astype(float)
    if len(res) == 0:
        return {"indices": []}

    mu = float(res.mean())
    sigma = float(res.std(ddof=1) + 1e-8)
    z = (res - mu) / sigma
    idx = np.where(np.abs(z.values) > threshold)[0].tolist()
    return {"indices": idx}
