from pathlib import Path

import pandas as pd

from nf_loto_platform.ml_analysis.reporting import (
    save_eval_report_html,
    save_eval_report_json,
    summarize_forecast_df,
)


def test_summarize_forecast_df_basic():
    df = pd.DataFrame(
        {
            "y": [1.0, 2.0, 3.0],
            "y_hat": [1.0, 2.5, 2.0],
        }
    )
    metrics = summarize_forecast_df(df)
    assert set(metrics.keys()) == {"mae", "rmse", "smape"}
    assert metrics["mae"] >= 0.0


def test_save_eval_report_html_and_json(tmp_path):
    metrics = {"mae": 1.23, "rmse": 2.34, "smape": 3.45}
    html_path = tmp_path / "eval_report.html"
    json_path = tmp_path / "eval_report.json"

    save_eval_report_html(metrics, html_path)
    save_eval_report_json(metrics, json_path)

    assert html_path.exists()
    assert json_path.exists()

    html_text = html_path.read_text(encoding="utf-8")
    assert "nf_loto eval report" in html_text

    data = pd.read_json(json_path)
    # JSON は dict なので read_json の結果は Series になる
    assert "mae" in data.index
