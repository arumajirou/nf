import importlib


def test_wandb_logger_module_present():
    spec = importlib.util.find_spec("nf_loto_platform.logging_ext.wandb_logger")
    assert spec is not None
