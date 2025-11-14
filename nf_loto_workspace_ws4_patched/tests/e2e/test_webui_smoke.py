import pytest

import nf_loto_platform.webui as webui


@pytest.mark.e2e
def test_webui_smoke_import_and_flag():
    """WebUI モジュールが import でき、可用性フラグが bool を返すことを確認する。"""
    assert webui.is_webui_available() in (True, False)
