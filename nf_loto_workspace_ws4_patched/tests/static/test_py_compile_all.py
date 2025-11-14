from pathlib import Path
import py_compile


def test_all_python_files_are_compilable():
    root = Path(__file__).resolve().parents[2]  # プロジェクトルート
    targets = []
    for sub in ("src", "apps", "tests"):
        base = root / sub
        if not base.exists():
            continue
        for py in base.rglob("*.py"):
            targets.append(py)
    assert targets, "No Python files found to compile"
    for py in targets:
        py_compile.compile(str(py), doraise=True)
