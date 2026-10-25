# PatientPath — Hospital Analytics Modern Data Stack

## Project Overview
PatientPath is a hospital operations and cost analytics project built to transform raw healthcare data into tested analytical models and an interactive dashboard.

## Architecture
Hospital Data Sources → Snowflake RAW → dbt Staging → dbt Intermediate → dbt Marts → Streamlit Dashboard

Apache Airflow orchestrates the daily dbt pipeline by running `dbt run` followed by `dbt test`.

## Technology Stack
- Snowflake: data warehouse and RAW data storage
- dbt Core and dbt-snowflake: data transformations and testing
- Apache Airflow: workflow orchestration
- Docker Compose: service deployment
- Streamlit: interactive dashboard

## Project Structure
```text
hospital-modern-stack/
├── airflow/
│   └── dags/
│       └── hospital_dbt_pipeline.py
├── hospital_analytics/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── app.py
│   ├── Dockerfile
│   └── dbt_project.yml
├── architecture.mmd
├── docker-compose.yml
└── README.md
```

## Data Transformation
- **Staging:** prepares source data for analysis.
- **Intermediate:** enriches encounters and procedures.
- **Marts:** provides patient and payer dimensions, encounter and procedure facts, and analytical summaries.

## Run the Project
1. Configure Snowflake connection details in your local dbt profile.
2. Configure Streamlit secrets locally in `hospital_analytics/.streamlit/secrets.toml`.
3. From the project root, build and start the services:

   ```bash
   docker compose up --build -d
   ```

4. Open the dashboard: http://localhost:8501
5. Open Airflow: http://localhost:8080

## Validate the Pipeline
In Airflow, trigger `hospital_dbt_pipeline` and confirm that both `dbt_run` and `dbt_test` succeed.

To inspect service status and logs:

```bash
docker compose ps
docker compose logs --tail=100
```

## Security
Do not commit credentials, passwords, private keys, or secret configuration files. Keep local credentials out of version control.

## Project Status
The unified Docker Compose services have started successfully, the dashboard has opened, and the Airflow dbt run and test tasks have succeeded in the current environment.
