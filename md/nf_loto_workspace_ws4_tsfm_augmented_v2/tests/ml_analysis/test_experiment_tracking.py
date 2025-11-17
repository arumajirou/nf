from types import SimpleNamespace

import pytest

from nf_loto_platform.ml_analysis.experiment_tracking import (
    RunInfo,
    log_metrics,
    start_run_with_params,
)


class _DummyRunInfo:
    def __init__(self, run_id: str):
        self.info = SimpleNamespace(run_id=run_id)


def test_start_run_with_params_no_mlflow(monkeypatch):
    # mlflow が無い環境でも例外が出ないこと
    monkeypatch.setitem(__import__("sys").modules, "mlflow", None)
    info = RunInfo(
        run_name="test_run",
        table_name="nf_loto_panel",
        loto="loto6",
        model_name="DummyModel",
        backend="local",
        horizon=10,
    )
    run_id = start_run_with_params(info, params={"a": 1})
    assert run_id is None


def test_start_run_with_params_with_fake_mlflow(monkeypatch):
    calls = {}

    def _start_run(run_name: str):
        calls["run_name"] = run_name
        return _DummyRunInfo(run_id="RUN123")

    def _log_params(params):
        calls["params"] = dict(params)

    def _set_tags(tags):
        calls["tags"] = dict(tags)

    fake_mlflow = SimpleNamespace(
        start_run=_start_run,
        log_params=_log_params,
        set_tags=_set_tags,
    )

    monkeypatch.setitem(__import__("sys").modules, "mlflow", fake_mlflow)

    info = RunInfo(
        run_name="test_run",
        table_name="nf_loto_panel",
        loto="loto6",
        model_name="DummyModel",
        backend="local",
        horizon=10,
    )
    run_id = start_run_with_params(info, params={"a": 1}, tags={"extra": "x"})
    assert run_id == "RUN123"
    assert calls["run_name"] == "test_run"
    assert calls["params"]["a"] == 1
    assert calls["tags"]["table_name"] == "nf_loto_panel"
    assert calls["tags"]["extra"] == "x"


def test_log_metrics_with_fake_mlflow(monkeypatch):
    calls = {}

    def _log_metrics(metrics, step=None):
        calls["metrics"] = dict(metrics)
        calls["step"] = step

    fake_mlflow = SimpleNamespace(
        log_metrics=_log_metrics,
    )
    monkeypatch.setitem(__import__("sys").modules, "mlflow", fake_mlflow)

    log_metrics("RUN123", metrics={"mae": 1.23}, step=10)
    assert calls["metrics"]["mae"] == 1.23
    assert calls["step"] == 10


def test_log_metrics_no_run_id(monkeypatch):
    # run_id が None の場合は何もしない
    fake_mlflow = SimpleNamespace(
        log_metrics=lambda metrics, step=None: (_ for _ in ()).throw(RuntimeError("should not be called"))
    )
    monkeypatch.setitem(__import__("sys").modules, "mlflow", fake_mlflow)

    log_metrics(None, metrics={"mae": 1.23}, step=10)
    # 例外が出なければ OK
