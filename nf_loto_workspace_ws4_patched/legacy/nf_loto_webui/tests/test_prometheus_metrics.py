import os
import sys
from pathlib import Path

# Ensure the project src/ is importable regardless of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from nf_monitoring import prometheus_metrics as pm


def test_init_metrics_server_idempotent():
    # Should not raise even when called multiple times.
    pm.init_metrics_server(port=8010)
    pm.init_metrics_server(port=8010)


def test_observe_run_start_and_end_increment_counters():
    if not getattr(pm, "_PROM_AVAILABLE", False):
        # In extremely stripped environments metrics may be disabled.
        return

    labels_started = pm.RUNS_STARTED.labels(model_name="m", backend="b")
    before_started = labels_started._value.get()
    pm.observe_run_start("m", "b")
    after_started = labels_started._value.get()
    assert after_started == before_started + 1

    labels_completed = pm.RUNS_COMPLETED.labels(model_name="m", backend="b", status="finished")
    before_completed = labels_completed._value.get()
    pm.observe_run_end("m", "b", status="finished", duration_seconds=0.5, resource_after=None)
    after_completed = labels_completed._value.get()
    assert after_completed == before_completed + 1

    # Histogram should have recorded at least one observation.
    hist = pm.RUN_DURATION.labels(model_name="m", backend="b", status="finished")
    # ``_sum.get()`` is an internal implementation detail but fine for tests.
    assert hist._sum.get() >= 0.5  # type: ignore[attr-defined]


def test_observe_train_step_updates_gauges():
    if not getattr(pm, "_PROM_AVAILABLE", False):
        return

    pm.observe_train_step("m2", "b2", train_loss=0.1, val_loss=0.2)
    train_val = pm.TRAIN_LOSS.labels(model_name="m2", backend="b2")._value.get()
    val_val = pm.VAL_LOSS.labels(model_name="m2", backend="b2")._value.get()
    assert train_val == 0.1
    assert val_val == 0.2
