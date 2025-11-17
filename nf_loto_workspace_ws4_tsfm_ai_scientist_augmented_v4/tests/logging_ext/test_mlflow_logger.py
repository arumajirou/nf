import importlib


def test_mlflow_logger_module_present():
    spec = importlib.util.find_spec("nf_loto_platform.logging_ext.mlflow_logger")
    assert spec is not None
