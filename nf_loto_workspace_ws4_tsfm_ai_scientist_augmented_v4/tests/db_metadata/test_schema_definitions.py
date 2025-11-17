from nf_loto_platform.db_metadata import schema_definitions


def test_schema_definitions_has_model_runs():
    # 最低限、nf_model_runs に関する定義が存在することだけ確認
    text = dir(schema_definitions)
    assert any("run" in name.lower() for name in text)
