"""実験トラッキングの薄いラッパー.

- MLflow がインストールされていればそれを利用し、無ければ no-op とする
- テストでは mlflow モジュールを monkeypatch して挙動を検証する

本番運用では、よりリッチなラッパー (tags, artifacts, model registry 連携など)
に拡張する前提の最小実装。
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping, Optional

import contextlib


@dataclass
class RunInfo:
    """1 回の学習・予測実行に関するメタ情報."""

    run_name: str
    table_name: str
    loto: str
    model_name: str
    backend: str
    horizon: int


def _get_mlflow():
    """mlflow が import できればそれを返し、できなければ None."""
    with contextlib.suppress(ImportError):
        import mlflow  # type: ignore

        return mlflow
    return None


def start_run_with_params(
    info: RunInfo,
    params: Mapping[str, Any],
    tags: Optional[Mapping[str, str]] = None,
) -> Optional[str]:
    """MLflow ランを開始し、params / tags を記録する.

    mlflow が利用できない環境では何もせず None を返す。
    戻り値は run_id または None。
    """
    mlflow = _get_mlflow()
    if mlflow is None:
        return None

    active_run = mlflow.start_run(run_name=info.run_name)
    run_id = active_run.info.run_id  # type: ignore[assignment]
    mlflow.log_params(dict(params))
    base_tags = {
        "table_name": info.table_name,
        "loto": info.loto,
        "model_name": info.model_name,
        "backend": info.backend,
        "horizon": str(info.horizon),
    }
    if tags:
        base_tags.update(tags)
    mlflow.set_tags(base_tags)
    return run_id


def log_metrics(run_id: Optional[str], metrics: Mapping[str, float], step: int | None = None) -> None:
    """MLflow にメトリクスを記録する.

    run_id が None の場合は no-op。
    """
    if run_id is None:
        return
    mlflow = _get_mlflow()
    if mlflow is None:
        return
    mlflow.log_metrics(dict(metrics), step=step)
