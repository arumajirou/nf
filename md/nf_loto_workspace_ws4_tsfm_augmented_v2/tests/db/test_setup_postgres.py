import importlib


def test_setup_postgres_module_exists():
    spec = importlib.util.find_spec("nf_loto_platform.db.setup_postgres")
    assert spec is not None
