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

from nf_logging import wandb_logger


def test_start_wandb_run_disabled_by_default(monkeypatch):
    monkeypatch.delenv("NF_WANDB_ENABLED", raising=False)
    ctx = wandb_logger.start_wandb_run(enabled=None, project="proj")
    assert ctx.enabled is False
    # All operations must be safe no-ops.
    ctx.log_metrics({"loss": 1.23}, step=1)
    ctx.set_summary({"status": "ok"})
    ctx.mark_failed(RuntimeError("boom"))
    ctx.finish()


def test_start_wandb_run_explicit_false(monkeypatch):
    monkeypatch.setenv("NF_WANDB_ENABLED", "1")
    ctx = wandb_logger.start_wandb_run(enabled=False, project="proj")
    assert ctx.enabled is False


def test_start_wandb_run_with_dummy_wandb(monkeypatch):
    # Enable W&B and inject a tiny fake implementation.
    class DummyRun:
        def __init__(self):
            self.logged = []
            self.summary = {}
            self.finished = False

        def log(self, metrics, step=None):
            self.logged.append((metrics, step))

        def finish(self):
            self.finished = True

    class DummyWandb(types.SimpleNamespace):
        def __init__(self):
            super().__init__()
            self.last_kwargs = None
            self.run = DummyRun()

        def init(self, **kwargs):
            self.last_kwargs = kwargs
            return self.run

    dummy = DummyWandb()
    monkeypatch.setenv("NF_WANDB_ENABLED", "1")
    monkeypatch.setattr(wandb_logger, "_WANDB_AVAILABLE", True, raising=False)
    monkeypatch.setattr(wandb_logger, "wandb", dummy, raising=False)

    ctx = wandb_logger.start_wandb_run(
        enabled=None,
        project="proj",
        run_name="run-1",
        config={"a": 1},
        tags=["tag1"],
        group="grp",
    )
    assert ctx.enabled is True

    ctx.log_metrics({"loss": 0.1}, step=5)
    ctx.set_summary({"key": "value"})
    ctx.mark_failed(RuntimeError("x"))
    ctx.finish()

    assert dummy.last_kwargs["project"] == "proj"
    assert dummy.run.logged[0][0]["loss"] == 0.1
    assert dummy.run.finished is True


def test_wandb_run_context_always_finishes(monkeypatch):
    # Similar to the previous test but uses the context manager.
    class DummyRun:
        def __init__(self):
            self.finished = False
            self.summary = {}

        def log(self, *_, **__):
            pass

        def finish(self):
            self.finished = True

    class DummyWandb(types.SimpleNamespace):
        def __init__(self):
            super().__init__()
            self.run = DummyRun()

        def init(self, **_):
            return self.run

    dummy = DummyWandb()
    monkeypatch.setenv("NF_WANDB_ENABLED", "1")
    monkeypatch.setattr(wandb_logger, "_WANDB_AVAILABLE", True, raising=False)
    monkeypatch.setattr(wandb_logger, "wandb", dummy, raising=False)

    with pytest.raises(RuntimeError):
        with wandb_logger.wandb_run_context(enabled=None) as ctx:
            assert ctx.enabled is True
            raise RuntimeError("inside")

    assert dummy.run.finished is True
