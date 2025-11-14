import importlib


def test_model_registry_module_present():
    spec = importlib.util.find_spec("nf_loto_platform.ml.model_registry")
    assert spec is not None
