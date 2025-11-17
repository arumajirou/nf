import importlib


def test_model_runner_module_present():
    spec = importlib.util.find_spec("nf_loto_platform.ml.model_runner")
    assert spec is not None
