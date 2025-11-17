from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

try:  # pragma: no cover - import validation is environment dependent
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    _JINJA_AVAILABLE = True
except Exception:  # pragma: no cover
    Environment = FileSystemLoader = select_autoescape = None  # type: ignore[assignment]
    _JINJA_AVAILABLE = False


def _build_env(template_dir: Path):
    if not _JINJA_AVAILABLE:
        raise RuntimeError(
            "jinja2 is not installed. Install it with `pip install jinja2` to use HTML reporting."
        )
    return Environment(  # type: ignore[call-arg]
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),  # type: ignore[call-arg]
    )


def render_run_report(
    template_dir: Path,
    output_path: Path,
    run_info: Dict[str, Any],
    metrics_df: pd.DataFrame,
    drift_df: Optional[pd.DataFrame] = None,
    feature_importance_df: Optional[pd.DataFrame] = None,
) -> Path:
    """Render a single‑run HTML report and write it to ``output_path``."""
    env = _build_env(template_dir)
    template = env.get_template("run_report.html")  # type: ignore[call-arg]

    html = template.render(
        generated_at=dt.datetime.utcnow().isoformat(),
        run=run_info,
        metrics=metrics_df.to_dict(orient="records"),
        drift=None if drift_df is None else drift_df.to_dict(orient="records"),
        feature_importance=None
        if feature_importance_df is None
        else feature_importance_df.to_dict(orient="records"),
    )

    output_path.write_text(html, encoding="utf-8")
    return output_path
# --- Simple helpers for tests and lightweight usage ---------------------

def render_simple_report(title: str, body: str) -> str:
    """シンプルな HTML レポート文字列を生成するユーティリティ。

    Jinja2 やテンプレートファイルに依存せず、テストや簡易用途で利用する。
    """
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
  </head>
  <body>
    <h1>{title}</h1>
    <div>{body}</div>
  </body>
</html>
"""


def write_report(output_path: "Path | str", html: str) -> "Path":
    """HTML 文字列を指定パスに書き出す軽量ヘルパー。

    Args:
        output_path: 出力先パス。
        html: HTML コンテンツ。

    Returns:
        pathlib.Path: 実際に書き出したパス。
    """
    path = Path(output_path)
    path.write_text(html, encoding="utf-8")
    return path
