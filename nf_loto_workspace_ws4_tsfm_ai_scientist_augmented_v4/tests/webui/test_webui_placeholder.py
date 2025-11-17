import nf_loto_platform.webui as webui


def test_webui_helper_api_exists_and_is_callable():
    """webui モジュールの薄いヘルパー API が存在し、呼び出せること。"""
    assert hasattr(webui, "is_webui_available")
    available = webui.is_webui_available()
    assert isinstance(available, bool)
