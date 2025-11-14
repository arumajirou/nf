import os
import sys
from pathlib import Path

# Ensure the project src/ is importable regardless of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import numpy as np
import pandas as pd

from nf_analysis import anomaly


def test_detect_zscore_anomalies_empty_series():
    res = anomaly.detect_zscore_anomalies(pd.Series([], dtype=float))
    assert res["indices"] == []


def test_detect_zscore_anomalies_flags_outliers():
    # Most points around 0, plus a strong outlier at index 50.
    data = np.concatenate([np.zeros(50), np.array([10.0]), np.zeros(49)])
    s = pd.Series(data)
    res = anomaly.detect_zscore_anomalies(s, threshold=3.0)
    assert 0 <= len(res["indices"]) <= len(s)
    # Strong outlier at index 50 must be detected.
    assert 50 in res["indices"]
