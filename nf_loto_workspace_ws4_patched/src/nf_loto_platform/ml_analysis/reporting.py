"""予測結果の要約・レポート生成ユーティリティ.

- summarize_forecast_df: DataFrame から代表的なメトリクスを計算
- save_eval_report_html: HTML レポートを保存
- save_eval_report_json: JSON レポートを保存

ここでは純粋関数 + 単純な HTML 生成に留め、テンプレートエンジンなどの
外部依存には踏み込まない。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import json

import pandas as pd

from .metrics import mae, rmse, smape


def summarize_forecast_df(
    df: pd.DataFrame,
    y_col: str = "y",
    yhat_col: str = "y_hat",
) -> dict[str, float]:
    """予測 DataFrame から基本メトリクスを計算する.

    Parameters
    ----------
    df:
        y_col, yhat_col を含む DataFrame。
    y_col, yhat_col:
        実績値・予測値の列名。

    Returns
    -------
    dict
        "mae", "rmse", "smape" をキーに持つ辞書。
    """
    if y_col not in df.columns or yhat_col not in df.columns:
        raise KeyError(f"columns {y_col!r}, {yhat_col!r} must exist in df.columns")

    y = df[y_col].to_numpy(dtype=float)
    yhat = df[yhat_col].to_numpy(dtype=float)

    return {
        "mae": mae(y, yhat),
        "rmse": rmse(y, yhat),
        "smape": smape(y, yhat),
    }


def save_eval_report_html(metrics: Mapping[str, Any], path: Path) -> None:
    """簡易な HTML レポートを生成して保存する."""
    path = Path(path)
    rows = "\n".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in sorted(metrics.items())
    )
    html = f"""<!DOCTYPE html>
    <html lang="ja">
      <head>
        <meta charset="utf-8" />
        <title>nf_loto eval report</title>
      </head>
      <body>
        <h1>nf_loto eval report</h1>
        <table border="1">
          <thead><tr><th>metric</th><th>value</th></tr></thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </body>
    </html>
    """
    path.write_text(html, encoding="utf-8")


def save_eval_report_json(metrics: Mapping[str, Any], path: Path) -> None:
    """メトリクス辞書を JSON として保存する."""
    path = Path(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(dict(metrics), f, ensure_ascii=False, indent=2)
