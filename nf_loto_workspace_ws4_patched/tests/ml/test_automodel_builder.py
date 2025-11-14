import importlib


def test_automodel_builder_module_present():
    spec = importlib.util.find_spec("nf_loto_platform.ml.automodel_builder")
    assert spec is not None
