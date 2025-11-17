import importlib


def test_loto_pg_store_module_exists():
    spec = importlib.util.find_spec("nf_loto_platform.db.loto_pg_store")
    assert spec is not None
