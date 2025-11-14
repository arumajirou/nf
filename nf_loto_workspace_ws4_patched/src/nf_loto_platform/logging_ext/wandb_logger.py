from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

try:  # pragma: no cover - import validation is environment dependent
    import wandb  # type: ignore[import]
    _WANDB_AVAILABLE = True
except Exception:  # pragma: no cover - if wandb is not installed
    wandb = None  # type: ignore[assignment]
    _WANDB_AVAILABLE = False


class WandbRunContext:
    """Thin wrapper around a W&B run.

    This object is intentionally tiny so that production code can depend
    on it without pulling in the heavy wandb dependency in tests.
    """

    def __init__(self, run: Optional[object]) -> None:
        self.run = run

    @property
    def enabled(self) -> bool:
        return self.run is not None

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None) -> None:
        if not self.enabled:
            return
        try:
            assert self.run is not None  # for type checkers
            self.run.log(metrics, step=step)  # type: ignore[call-arg]
        except Exception:  # pragma: no cover - defensive logging
            logger.exception("Failed to log metrics to W&B.")

    def set_summary(self, summary: Dict[str, Any]) -> None:
        if not self.enabled:
            return
        try:
            assert self.run is not None
            for key, value in summary.items():
                self.run.summary[key] = value  # type: ignore[index]
        except Exception:  # pragma: no cover - defensive logging
            logger.exception("Failed to update W&B summary.")

    def mark_failed(self, error: BaseException) -> None:
        if not self.enabled:
            return
        try:
            assert self.run is not None
            self.run.summary["status"] = "failed"  # type: ignore[index]
            self.run.summary["error"] = str(error)  # type: ignore[index]
        except Exception:  # pragma: no cover - defensive logging
            logger.exception("Failed to mark W&B run as failed.")

    def finish(self) -> None:
        if not self.enabled:
            return
        try:
            assert self.run is not None
            self.run.finish()  # type: ignore[call-arg]
        except Exception:  # pragma: no cover - defensive logging
            logger.exception("Failed to finish W&B run.")


def _should_enable(explicit: Optional[bool]) -> bool:
    """Decide whether W&B logging should be enabled.

    Precedence:
    1. explicit flag if given
    2. NF_WANDB_ENABLED environment variable ("1" means enabled)
    """
    if explicit is not None:
        return bool(explicit)
    return os.getenv("NF_WANDB_ENABLED", "0") == "1"


def start_wandb_run(
    enabled: Optional[bool] = None,
    project: Optional[str] = None,
    entity: Optional[str] = None,
    run_name: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
    tags: Optional[list[str]] = None,
    group: Optional[str] = None,
) -> WandbRunContext:
    """Start a W&B run if W&B is available and enabled.

    In all other cases a disabled :class:`WandbRunContext` is returned.
    """
    if not _WANDB_AVAILABLE or not _should_enable(enabled):
        logger.info("W&B logging is disabled or wandb is not installed.")
        return WandbRunContext(run=None)

    # Lazily import inside the branch so tests can monkeypatch ``wandb`` cleanly.
    try:
        assert wandb is not None  # type: ignore[truthy-function]
    except AssertionError:  # pragma: no cover - extreme edge case
        logger.warning("wandb module unexpectedly missing at runtime.")
        return WandbRunContext(run=None)

    project = project or os.getenv("NF_WANDB_PROJECT", "nf_loto_webui")
    entity = entity or os.getenv("NF_WANDB_ENTITY")
    config = config or {}
    tags = tags or []

    try:
        run = wandb.init(  # type: ignore[call-arg]
            project=project,
            entity=entity,
            name=run_name,
            config=config,
            tags=tags,
            group=group,
        )
        logger.info("Started W&B run project=%s name=%s", project, run_name)
        return WandbRunContext(run=run)
    except Exception:  # pragma: no cover - network or auth problems
        logger.exception("Failed to initialise W&B run. Falling back to disabled context.")
        return WandbRunContext(run=None)


@contextmanager
def wandb_run_context(**kwargs: Any):
    """Context manager that always calls ``finish`` at the end.

    Examples
    --------
    >>> from nf_logging.wandb_logger import wandb_run_context
    >>> with wandb_run_context(enabled=False) as ctx:
    ...     assert not ctx.enabled
    """
    ctx = start_wandb_run(**kwargs)
    try:
        yield ctx
    finally:
        ctx.finish()
