from pathlib import Path
import importlib

def test_db_config_module_exists():
    spec = importlib.util.find_spec("nf_loto_platform.db.db_config")
    assert spec is not None
