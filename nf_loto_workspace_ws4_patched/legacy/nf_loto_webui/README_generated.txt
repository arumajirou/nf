This directory contains a minimal implementation of the additional
MLOps utilities discussed in the design:

- nf_logging.wandb_logger / mlflow_logger
- nf_monitoring.prometheus_metrics / resource_monitor
- nf_analysis.drift / anomaly / model_stats
- nf_reports.html_reporter
- nf_metadata.schema_definitions + SQL migration

A pytest test-suite is provided under tests/ and can be executed with:

    cd nf_loto_webui
    pytest -q
