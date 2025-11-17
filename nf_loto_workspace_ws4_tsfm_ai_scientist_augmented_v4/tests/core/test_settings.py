from pathlib import Path
from nf_loto_platform.core import settings


def test_load_db_config_returns_dict(tmp_path, monkeypatch):
    # config/db.yaml が無い環境でも dict を返すことを確認
    cfg = settings.load_db_config()
    assert isinstance(cfg, dict)
