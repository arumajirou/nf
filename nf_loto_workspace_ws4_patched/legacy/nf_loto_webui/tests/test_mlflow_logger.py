import os
import sys
from pathlib import Path

# Ensure the project src/ is importable regardless of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import types

import pytest

from nf_logging import mlflow_logger


def test_mlflow_run_context_disabled(monkeypatch):
    monkeypatch.delenv("NF_MLFLOW_ENABLED", raising=False)
    with mlflow_logger.mlflow_run_context(enabled=None) as run:
        assert run is None


def test_mlflow_run_context_with_dummy_mlflow(monkeypatch):
    class DummyMLflow(types.SimpleNamespace):
        def __init__(self):
            super().__init__()
            self.experiments = []
            self.started = []
            self.ended = 0
            self.tags = []
            self.params = []

        def set_experiment(self, name):
            self.experiments.append(name)

        class _Run:
            def __init__(self, name):
                self.name = name

        def start_run(self, run_name=None):
            run = self._Run(run_name)
            self.started.append(run_name)
            return run

        def set_tags(self, tags):
            self.tags.append(tags)

        def log_params(self, params):
            self.params.append(params)

        def end_run(self):
            self.ended += 1

    dummy = DummyMLflow()
    monkeypatch.setenv("NF_MLFLOW_ENABLED", "1")
    monkeypatch.setattr(mlflow_logger, "_MLFLOW_AVAILABLE", True, raising=False)
    monkeypatch.setattr(mlflow_logger, "mlflow", dummy, raising=False)

    with mlflow_logger.mlflow_run_context(
        enabled=None,
        run_name="run-x",
        experiment_name="exp-1",
        tags={"k": "v"},
        params={"p": 1},
    ) as run:
        # The run object is provided by DummyMLflow._Run
        assert run is not None
        assert run.name == "run-x"

    assert dummy.experiments == ["exp-1"]
    assert dummy.started == ["run-x"]
    assert dummy.tags == [{"k": "v"}]
    assert dummy.params == [{"p": 1}]
    assert dummy.ended == 1


def test_mlflow_run_context_swallows_internal_errors(monkeypatch):
    class FailingMLflow(types.SimpleNamespace):
        def start_run(self, run_name=None):
            raise RuntimeError("boom")

    monkeypatch.setenv("NF_MLFLOW_ENABLED", "1")
    monkeypatch.setattr(mlflow_logger, "_MLFLOW_AVAILABLE", True, raising=False)
    monkeypatch.setattr(mlflow_logger, "mlflow", FailingMLflow(), raising=False)

    # Even if MLflow explodes, the context should yield None and not raise.
    with mlflow_logger.mlflow_run_context(enabled=None) as run:
        assert run is None
