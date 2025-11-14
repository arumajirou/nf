from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

try:  # pragma: no cover - import validation is environment dependent
    import mlflow  # type: ignore[import]
    _MLFLOW_AVAILABLE = True
except Exception:  # pragma: no cover - if mlflow is not installed
    mlflow = None  # type: ignore[assignment]
    _MLFLOW_AVAILABLE = False


def _should_enable(explicit: Optional[bool]) -> bool:
    if explicit is not None:
        return bool(explicit)
    return os.getenv("NF_MLFLOW_ENABLED", "0") == "1"


@contextmanager
def mlflow_run_context(
    enabled: Optional[bool] = None,
    run_name: Optional[str] = None,
    experiment_name: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
):
    """Context manager to safely handle an MLflow run.

    When MLflow is not available or disabled, this becomes a no-op context
    that simply yields ``None``.
    """
    if not _MLFLOW_AVAILABLE or not _should_enable(enabled):
        yield None
        return

    assert mlflow is not None  # type: ignore[truthy-function]

    try:
        if experiment_name:
            mlflow.set_experiment(experiment_name)
        run = mlflow.start_run(run_name=run_name)
        if tags:
            mlflow.set_tags(tags)
        if params:
            mlflow.log_params(params)
        yield run
    except Exception:  # pragma: no cover - defensive logging
        logger.exception("Error while starting MLflow run.")
        yield None
    finally:
        try:
            if _MLFLOW_AVAILABLE and _should_enable(enabled):
                mlflow.end_run()
        except Exception:  # pragma: no cover
            logger.exception("Failed to end MLflow run.")
