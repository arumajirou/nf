from nf_loto_platform.monitoring import resource_monitor


def test_resource_monitor_returns_dict_like():
    info = resource_monitor.collect_resource_usage()
    assert isinstance(info, dict)
    # キー名がいくつか存在することをざっくり確認
    assert any("cpu" in k.lower() for k in info.keys())
