import importlib


def test_loto_etl_modules_exist():
    for mod in ("nf_loto_platform.db.loto_etl", "nf_loto_platform.db.loto_etl_updated"):
        spec = importlib.util.find_spec(mod)
        assert spec is not None
