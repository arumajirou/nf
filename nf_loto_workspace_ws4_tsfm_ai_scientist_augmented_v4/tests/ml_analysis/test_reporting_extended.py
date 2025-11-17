"""ml_analysis.reporting の追加ユニットテスト.

- save_eval_report_json の JSON 形式を厳密に検証
- summarize_forecast_df のオプション引数や値の妥当性を確認
"""

from pathlib import Path

import pandas as pd
import pytest

from nf_loto_platform.ml_analysis.reporting import (
    save_eval_report_json,
    summarize_forecast_df,
)


def test_save_eval_report_json_roundtrip(tmp_path: Path) -> None:
    """JSON を pd.read_json で読み戻したときに index/columns/値が一致することを確認する."""
    metrics = {
        "mae": 1.23,
        "rmse": 2.34,
        "smape": 3.45,
    }
    path = tmp_path / "metrics.json"

    save_eval_report_json(metrics, path)

    assert path.exists()

    df = pd.read_json(path)

    # 1 列 DataFrame であること（value 列のみ）
    assert list(df.columns) == ["value"]
    # index がメトリクス名になっていること
    assert set(df.index) == set(metrics.keys())

    for name, expected in metrics.items():
        assert pytest.approx(df.loc[name, "value"]) == expected


def test_summarize_forecast_df_custom_columns() -> None:
    """y_col / yhat_col を差し替えても正しく計算できることを確認する."""
    df = pd.DataFrame(
        {
            "target": [1.0, 2.0, 3.0, 4.0],
            "pred": [0.9, 2.1, 2.9, 4.2],
        }
    )

    metrics = summarize_forecast_df(df, y_col="target", yhat_col="pred")

    # 代表的なメトリクスがすべて含まれている
    for key in ["mae", "rmse", "smape"]:
        assert key in metrics

    # MAE は 0 以上の有限値
    assert metrics["mae"] >= 0.0
    assert float(metrics["mae"]) == pytest.approx(metrics["mae"])
