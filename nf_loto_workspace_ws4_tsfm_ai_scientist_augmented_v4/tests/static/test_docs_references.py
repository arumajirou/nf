from pathlib import Path


def test_docs_key_files_exist():
    root = Path(__file__).resolve().parents[2]
    docs = root / "docs"
    assert docs.exists()
    for name in ("DESIGN_OVERVIEW.md", "API_REFERENCE.md", "IMPLEMENTATION_PLAN.md"):
        assert (docs / name).exists()
