from __future__ import annotations

import importlib
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
PKG_ROOT = SRC_ROOT / "nf_loto_platform"


# parametrize 時点で __pycache__ 配下は除外し、テスト関数内での skip を発生させない
MODULE_PATHS = [
    p for p in sorted(PKG_ROOT.rglob("*.py")) if "__pycache__" not in p.parts
]


@pytest.mark.parametrize("module_path", MODULE_PATHS)
def test_all_nf_loto_platform_modules_importable(module_path: Path):
    rel = module_path.relative_to(SRC_ROOT)
    module_name = ".".join(rel.with_suffix("").parts)

    try:
        importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001
        pytest.fail(f"モジュール {module_name!r} の import に失敗しました: {exc!r}")
