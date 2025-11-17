import pandas as pd

from nf_loto_platform.features import add_lag_feature


def test_add_lag_feature_basic_contract():
    """ラグ特徴量ユーティリティの基本的な契約を確認する。"""
    df = pd.DataFrame(
        {
            "unique_id": ["A", "A", "A"],
            "ds": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "y": [1.0, 2.0, 3.0],
        }
    )

    out = add_lag_feature(df, lag=1)
    assert set(df.columns).issubset(out.columns)
    assert "y_lag1" in out.columns
    # 先頭要素は NaN、2 行目以降は 1 つ前と一致する
    assert out.loc[0, "y_lag1"] != out.loc[1, "y_lag1"]
    assert out.loc[2, "y_lag1"] == df.loc[1, "y"]
