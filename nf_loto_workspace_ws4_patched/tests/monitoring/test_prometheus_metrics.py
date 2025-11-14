import importlib
import inspect

import nf_loto_platform.monitoring.prometheus_metrics as pm


def test_prometheus_metrics_module_present():
    spec = importlib.util.find_spec("nf_loto_platform.monitoring.prometheus_metrics")
    assert spec is not None


def test_prometheus_metrics_public_api_contains_expected_functions():
    """Basic API contract: required functions must exist.

    This helps detect accidental renames/removals that would break callers
    like nf_loto_platform.ml.model_runner.
    """
    funcs = {name for name, obj in inspect.getmembers(pm, inspect.isfunction)}
    required = {
        "init_metrics_server",
        "observe_run_start",
        "observe_run_end",
        "observe_run_error",
        "observe_train_step",
    }
    assert required.issubset(funcs)


def test_prometheus_metrics_functions_are_noop_without_prom_client(monkeypatch):
    """When prometheus_client is not available, helpers must safely no-op."""
    # Force the module into "prometheus not available" mode.
    monkeypatch.setattr(pm, "_PROM_AVAILABLE", False, raising=False)

    # None of these calls should raise, even without prometheus_client installed.
    pm.init_metrics_server(port=9999)
    pm.observe_run_start(model_name="TestModel", backend="local")
    pm.observe_run_end(
        model_name="TestModel",
        backend="local",
        status="success",
        duration_seconds=0.1,
        resource_after=None,
    )
    pm.observe_run_error(model_name="TestModel", backend="local")
    pm.observe_train_step(
        model_name="TestModel",
        backend="local",
        train_loss=0.5,
        val_loss=0.4,
    )
