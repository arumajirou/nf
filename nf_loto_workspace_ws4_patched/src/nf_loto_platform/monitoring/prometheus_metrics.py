from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:  # pragma: no cover - import validation is environment dependent
    from prometheus_client import Counter, Histogram, Gauge, start_http_server
    _PROM_AVAILABLE = True
except Exception:  # pragma: no cover
    Counter = Histogram = Gauge = None  # type: ignore[assignment]
    start_http_server = None  # type: ignore[assignment]
    _PROM_AVAILABLE = False

_METRICS_SERVER_STARTED = False

if _PROM_AVAILABLE:
    RUNS_STARTED = Counter(
        "nf_model_runs_started_total",
        "Total number of model runs started.",
        ["model_name", "backend"],
    )
    RUNS_COMPLETED = Counter(
        "nf_model_runs_completed_total",
        "Total number of model runs completed by status.",
        ["model_name", "backend", "status"],
    )
    RUN_DURATION = Histogram(
        "nf_model_run_duration_seconds",
        "Duration of model runs in seconds.",
        ["model_name", "backend", "status"],
    )
    TRAIN_LOSS = Gauge(
        "nf_model_train_loss",
        "Latest training loss value.",
        ["model_name", "backend"],
    )
    VAL_LOSS = Gauge(
        "nf_model_val_loss",
        "Latest validation loss value.",
        ["model_name", "backend"],
    )
else:  # pragma: no cover - when prometheus_client is entirely unavailable
    RUNS_STARTED = RUNS_COMPLETED = RUN_DURATION = TRAIN_LOSS = VAL_LOSS = None  # type: ignore[assignment]


def init_metrics_server(port: int = 8000) -> None:
    """Start the Prometheus metrics HTTP server once.

    Safe to call multiple times.
    """
    global _METRICS_SERVER_STARTED
    if not _PROM_AVAILABLE:
        logger.info("prometheus_client is not installed; metrics server disabled.")
        return
    if _METRICS_SERVER_STARTED:
        return
    try:
        start_http_server(port)  # type: ignore[call-arg]
        _METRICS_SERVER_STARTED = True
        logger.info("Prometheus metrics server started on port %d", port)
    except Exception:  # pragma: no cover - port clashes etc.
        logger.exception("Failed to start Prometheus metrics server.")


def observe_run_start(model_name: str, backend: str) -> None:
    if not _PROM_AVAILABLE:
        return
    RUNS_STARTED.labels(model_name=model_name, backend=backend).inc()  # type: ignore[call-arg]


def observe_run_end(
    model_name: str,
    backend: str,
    status: str,
    duration_seconds: float,
    resource_after: Optional[dict] = None,
) -> None:
    if not _PROM_AVAILABLE:
        return
    RUNS_COMPLETED.labels(  # type: ignore[call-arg]
        model_name=model_name,
        backend=backend,
        status=status,
    ).inc()
    RUN_DURATION.labels(  # type: ignore[call-arg]
        model_name=model_name,
        backend=backend,
        status=status,
    ).observe(duration_seconds)


def observe_train_step(
    model_name: str,
    backend: str,
    train_loss: Optional[float] = None,
    val_loss: Optional[float] = None,
) -> None:
    """Update gauges for train/validation loss.

    Any value set to ``None`` is ignored.
    """
    if not _PROM_AVAILABLE:
        return
    if train_loss is not None:
        TRAIN_LOSS.labels(model_name=model_name, backend=backend).set(train_loss)  # type: ignore[call-arg]
    if val_loss is not None:
        VAL_LOSS.labels(model_name=model_name, backend=backend).set(val_loss)  # type: ignore[call-arg]


def observe_run_error(model_name: str, backend: str) -> None:
    """Observe that a run ended with an error.

    This is intentionally lightweight: environments without ``prometheus_client``
    simply no-op. In the future this function can be extended to increment
    an error counter or set error-related gauges.

    Args:
        model_name: Logical name of the forecasting model.
        backend: Execution backend (e.g. "local", "ray").
    """
    if not _PROM_AVAILABLE:
        return
    # At the moment we do not maintain a dedicated error metric.
    # This hook exists so that callers can reliably emit a signal when
    # a run fails, and we can later attach concrete Prometheus counters
    # without changing the public API.
    return
