import pandas as pd
import pytest

from nf_loto_platform.features import add_lag_feature


@pytest.mark.integration
def test_feature_pipeline_simple_integration():
    """特徴量生成ユーティリティが小さなパネルで end-to-end に動くことを確認する。"""
    df = pd.DataFrame(
        {
            "unique_id": ["A", "A", "B", "B"],
            "ds": pd.to_datetime(
                ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-02"]
            ),
            "y": [10.0, 11.0, 20.0, 21.0],
        }
    )

    out = add_lag_feature(df, lag=1)
    assert len(out) == len(df)
    assert "y_lag1" in out.columns
    # グループごとにラグがずれていないこと
    a_rows = out[out["unique_id"] == "A"].sort_values("ds")
    b_rows = out[out["unique_id"] == "B"].sort_values("ds")
    assert a_rows["y_lag1"].iloc[1] == 10.0
    assert b_rows["y_lag1"].iloc[1] == 20.0
