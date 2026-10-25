from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="hospital_dbt_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["hospital", "dbt"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "mkdir -p /tmp/dbt-logs /tmp/dbt-target && "
            "cd /opt/dbt/hospital_analytics && "
            "dbt run "
            "--profiles-dir /home/airflow/.dbt "
            "--log-path /tmp/dbt-logs "
            "--target-path /tmp/dbt-target"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "mkdir -p /tmp/dbt-logs /tmp/dbt-target && "
            "cd /opt/dbt/hospital_analytics && "
            "dbt test "
            "--profiles-dir /home/airflow/.dbt "
            "--log-path /tmp/dbt-logs "
            "--target-path /tmp/dbt-target"
        ),
    )

    dbt_run >> dbt_test
