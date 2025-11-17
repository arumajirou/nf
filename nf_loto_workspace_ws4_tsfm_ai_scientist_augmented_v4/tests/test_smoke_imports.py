def test_import_package():
    import nf_loto_platform  # noqa: F401


def test_import_training_pipeline():
    from nf_loto_platform.pipelines.training_pipeline import run_legacy_nf_auto_runner  # noqa: F401
