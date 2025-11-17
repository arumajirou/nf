from __future__ import annotations
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[3]

def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def load_db_config() -> dict:
    """config/db.yaml または db.yaml.template を読み込むヘルパー。"""
    for name in ("db.yaml", "db.yaml.template"):
        cfg_path = BASE_DIR / "config" / name
        data = load_yaml(cfg_path)
        if data:
            return data
    return {}
