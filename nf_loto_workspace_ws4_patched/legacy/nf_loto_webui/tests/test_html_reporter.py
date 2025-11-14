import os
import sys
from pathlib import Path

# Ensure the project src/ is importable regardless of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from pathlib import Path

import pandas as pd

from nf_reports import html_reporter


def test_render_run_report(tmp_path: Path):
    template_dir = tmp_path / "templates"
    template_dir.mkdir()

    # Minimal Jinja2 template.
    (template_dir / "run_report.html").write_text(
        """<!DOCTYPE html>
        <html><body>
        <h1>Run Report: {{ run.run_id }}</h1>
        <p>Model: {{ run.model_name }}</p>
        {% for row in metrics %}
          <div class="metric">{{ row.name }}={{ row.value }}</div>
        {% endfor %}
        </body></html>
        """,
        encoding="utf-8",
    )

    run_info = {"run_id": 1, "model_name": "NHITS"}
    metrics_df = pd.DataFrame([{"name": "mse", "value": 0.123}])

    output_path = tmp_path / "report.html"
    result_path = html_reporter.render_run_report(
        template_dir=template_dir,
        output_path=output_path,
        run_info=run_info,
        metrics_df=metrics_df,
    )

    assert result_path == output_path
    html = output_path.read_text(encoding="utf-8")
    assert "Run Report: 1" in html
    assert "Model: NHITS" in html
    assert "mse=0.123" in html
