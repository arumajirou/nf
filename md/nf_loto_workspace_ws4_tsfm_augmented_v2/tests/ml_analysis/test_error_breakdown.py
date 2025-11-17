import numpy as np
import pandas as pd

from nf_loto_platform.ml_analysis.error_breakdown import (
    build_error_breakdown,
    build_time_series_metrics,
)


def _make_dummy_df() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=6, freq="D")
    return pd.DataFrame(
        {
            "loto": ["loto6"] * 3 + ["loto7"] * 3,
            "unique_id": ["A", "A", "B", "A", "B", "B"],
            "ds": dates,
            "y": np.array([1.0, 2.0, 3.0, 2.0, 4.0, 6.0]),
            "y_hat": np.array([1.0, 2.5, 2.5, 1.5, 4.5, 5.0]),
        }
    )


def test_build_error_breakdown_basic():
    df = _make_dummy_df()
    out = build_error_breakdown(df, group_keys=("loto", "unique_id"))

    # group_keys がそのまま出てくること
    assert set(["loto", "unique_id", "mae", "rmse", "smape"]).issuperset(out.columns)

    # グループ数が期待通りか（loto6-A, loto6-B, loto7-A, loto7-B の4グループ）
    assert len(out) == 4

    # 少なくとも 1 グループでは誤差が 0 でないこと（テストとしての sanity check）
    assert (out["mae"] > 0).any()


def test_build_time_series_metrics_basic():
    df = _make_dummy_df()
    out = build_time_series_metrics(df, freq="3D")

    # ds + metrics が含まれていること
    assert set(["ds", "mae", "rmse", "smape"]).issuperset(out.columns)

    # 3 日ごとの resample なので 2 行のはず
    assert len(out) == 2

    # 誤差が全て 0 ではないこと
    assert (out["mae"] > 0).any()
