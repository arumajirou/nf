
"""
nf_loto_platform 環境・レイアウト・インポート契約を検証するシステムレベルテスト。

目的:
- プロジェクトルート / src / notebooks / apps のディレクトリ構造が想定どおりかを確認
- notebooks ディレクトリからの推奨 import パターンが成立することを確認
- WebUI ディレクトリからも同様に import できる前提が成り立つことを確認

このテストが通っていれば、Notebook からの `ModuleNotFoundError: no module named 'nf_loto_platform'`
のような「レイアウト違い起因」の事故は、基本的に起こらない前提になります
（あとは Notebook 側で推奨パターンどおりに sys.path を設定すればよい状態）。
"""

from __future__ import annotations

from pathlib import Path
import importlib
import sys
from typing import Iterator
import contextlib


# テストファイルの位置から、プロジェクトルートを逆算する
# tests/system/test_environment_contract.py
# → parents[0] = system, [1] = tests, [2] = project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
WEBUI_DIR = PROJECT_ROOT / "apps" / "webui_streamlit"


@contextlib.contextmanager
def _temporary_sys_path(path: Path) -> Iterator[None]:
    """sys.path に一時的にパスを追加するコンテキストマネージャ。"""
    original = list(sys.path)
    sys.path.insert(0, str(path))
    try:
        yield
    finally:
        # テスト実行後に必ず元の状態へ戻す
        sys.path[:] = original


def test_project_layout_is_expected():
    """プロジェクトの基本ディレクトリ構造が想定どおりであることを検証。"""
    assert PROJECT_ROOT.exists(), f"PROJECT_ROOT が存在しません: {PROJECT_ROOT}"
    assert SRC_ROOT.exists(), f"src ディレクトリが見つかりません: {SRC_ROOT}"
    assert (SRC_ROOT / "nf_loto_platform").is_dir(), "nf_loto_platform パッケージが src 配下に存在しません"
    assert NOTEBOOKS_DIR.is_dir(), f"notebooks ディレクトリが見つかりません: {NOTEBOOKS_DIR}"
    assert WEBUI_DIR.is_dir(), f"apps/webui_streamlit ディレクトリが見つかりません: {WEBUI_DIR}"


def test_notebooks_import_contract():
    """notebooks 配下からの推奨 import パターンが成立することを検証。

    Notebook から推奨されるパターン:

    ```python
    from pathlib import Path
    import sys

    NOTEBOOK_PATH = Path.cwd()
    PROJECT_ROOT = NOTEBOOK_PATH.parent
    SRC_ROOT = PROJECT_ROOT / "src"

    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))

    import nf_loto_platform
    ```
    """
    assert NOTEBOOKS_DIR.is_dir(), f"notebooks ディレクトリが見つかりません: {NOTEBOOKS_DIR}"

    # Notebook から見たパス解決をシミュレート
    notebook_path = NOTEBOOKS_DIR / "dummy.ipynb"
    project_root_from_nb = notebook_path.parent.parent
    src_root_from_nb = project_root_from_nb / "src"

    assert project_root_from_nb == PROJECT_ROOT, "Notebook から見た PROJECT_ROOT の逆算がずれています"
    assert src_root_from_nb == SRC_ROOT, "Notebook から見た SRC_ROOT の逆算がずれています"
    assert (src_root_from_nb / "nf_loto_platform").is_dir(), "SRC_ROOT から nf_loto_platform が見つかりません"

    # 実際に sys.path に SRC_ROOT を追加したうえで import が通ることを確認
    with _temporary_sys_path(src_root_from_nb):
        module = importlib.import_module("nf_loto_platform")
        assert module is not None
        # せめて __file__ を持っていることだけ確認しておく
        assert hasattr(module, "__file__")


def test_webui_import_contract():
    """apps/webui_streamlit 配下からの import 契約を検証。

    webui 配下からの推奨パターン（例）:

    ```python
    from pathlib import Path
    import sys

    APP_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = APP_DIR.parent.parent
    SRC_ROOT = PROJECT_ROOT / "src"

    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))

    import nf_loto_platform
    ```
    """
    assert WEBUI_DIR.is_dir(), f"apps/webui_streamlit ディレクトリが見つかりません: {WEBUI_DIR}"

    app_dir = WEBUI_DIR
    project_root_from_app = app_dir.parent.parent
    src_root_from_app = project_root_from_app / "src"

    assert project_root_from_app == PROJECT_ROOT, "WebUI から見た PROJECT_ROOT の逆算がずれています"
    assert src_root_from_app == SRC_ROOT, "WebUI から見た SRC_ROOT の逆算がずれています"
    assert (src_root_from_app / "nf_loto_platform").is_dir(), "SRC_ROOT から nf_loto_platform が見つかりません"

    with _temporary_sys_path(src_root_from_app):
        module = importlib.import_module("nf_loto_platform")
        assert module is not None
        assert hasattr(module, "__file__")
