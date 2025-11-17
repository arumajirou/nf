from nf_loto_platform.core import settings


def test_load_db_config_returns_dict():
    cfg = settings.load_db_config()
    assert isinstance(cfg, dict)
