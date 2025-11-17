import importlib


def test_postgres_manager_module_exists():
    spec = importlib.util.find_spec("nf_loto_platform.db.postgres_manager")
    assert spec is not None
