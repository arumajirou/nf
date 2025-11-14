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

from nf_analysis import drift


def test_compute_univariate_drift_identical_series():
    s = pd.Series(np.random.RandomState(0).normal(size=100))
    metrics = drift.compute_univariate_drift(s, s.copy())
    assert abs(metrics["mean_diff"]) < 1e-8
    assert abs(metrics["std_ratio"] - 1.0) < 1e-6
    assert metrics["kl_div"] < 1e-6


def test_compute_univariate_drift_shifted_series():
    base = pd.Series(np.zeros(100))
    current = pd.Series(np.ones(100))
    metrics = drift.compute_univariate_drift(base, current)
    assert metrics["mean_diff"] > 0.5
    assert metrics["std_ratio"] >= 0.0
    assert metrics["kl_div"] > 0.0


def test_compute_dataframe_drift_multiple_columns():
    base_df = pd.DataFrame({"a": [0.0, 1.0, 2.0], "b": [1.0, 1.0, 1.0]})
    current_df = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": [1.0, 1.0, 1.0]})
    df = drift.compute_dataframe_drift(base_df, current_df)
    assert set(df["column_name"]) == {"a", "b"}
    a_row = df[df["column_name"] == "a"].iloc[0]
    b_row = df[df["column_name"] == "b"].iloc[0]
    assert a_row["mean_diff"] != 0.0
    # Column b is constant so its KL should be ~0.
    assert b_row["kl_div"] < 1e-6
