"""Contract tests for nf_loto_platform.ml.model_runner.

These tests avoid heavy training runs and instead focus on the public
Python API that other parts of the system rely on.
"""

import importlib
import inspect
from types import ModuleType


MODULE_NAME = "nf_loto_platform.ml.model_runner"


def _import_module() -> ModuleType:
    spec = importlib.util.find_spec(MODULE_NAME)
    assert spec is not None, f"Module {MODULE_NAME!r} should be importable"
    module = importlib.import_module(MODULE_NAME)
    return module


def test_model_runner_exposes_core_entrypoints():
    module = _import_module()
    # The high‑level API used from pipelines / CLI
    assert hasattr(module, "run_loto_experiment")
    assert hasattr(module, "sweep_loto_experiments")

    run_fn = module.run_loto_experiment
    sweep_fn = module.sweep_loto_experiments

    assert inspect.isfunction(run_fn)
    assert inspect.isfunction(sweep_fn)


def test_model_runner_has_dataclass_result_type():
    module = _import_module()
    assert hasattr(module, "LotoExperimentResult")
    result_type = module.LotoExperimentResult
    # Dataclasses expose __dataclass_fields__ when properly defined.
    assert hasattr(result_type, "__dataclass_fields__")
