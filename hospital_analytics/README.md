PatientPath — Hospital Analytics Modern Data Stack

Project Overview

PatientPath is a hospital analytics project built to transform healthcare data into useful insights about patient encounters, procedures, and healthcare costs.

The project uses Snowflake for data storage, dbt for data transformation and testing, Apache Airflow for pipeline orchestration, and Streamlit for interactive data visualization.

Architecture

1. Snowflake RAW: Stores the source healthcare datasets.
2. dbt Staging: Cleans and prepares raw data.
3. dbt Intermediate: Combines and transforms data for analytical use.
4. dbt Marts: Provides fact and dimension models for reporting.
5. Apache Airflow: Orchestrates the dbt run and dbt test tasks.
6. Streamlit Dashboard: Displays hospital analytics through KPIs, charts, and filters.

See "../architecture.mmd" for the architecture diagram source.

Technology Stack

- Snowflake
- dbt Core and dbt-snowflake
- Apache Airflow
- Docker and Docker Compose
- Python
- Streamlit

Project Structure

hospital-modern-stack/
├── architecture.mmd
├── airflow/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── dags/
└── hospital_analytics/
    ├── app.py
    ├── Dockerfile
    ├── docker-compose.yml
    ├── dbt_project.yml
    └── models/
        ├── staging/
        ├── intermediate/
        └── marts/

Data Transformation

The dbt project organizes transformations into three layers:

- Staging: Prepares source data for transformation.
- Intermediate: Applies business logic and combines related datasets.
- Marts: Organizes analytical data into fact and dimension models.

The models are tested using dbt tests, including data quality and relationship checks where configured.

Pipeline Orchestration

The Airflow DAG runs the following tasks in order:

1. "dbt_run" — builds the dbt models.
2. "dbt_test" — runs the dbt tests after the models are built.

The DAG is configured for daily scheduling.

Dashboard

The Streamlit application presents hospital analytics using KPI metrics, charts, and interactive filters. It connects to Snowflake to query analytical data.

When running locally, the dashboard is intended to be available at:

"http://localhost:8501"

Airflow is intended to be available at:

"http://localhost:8080"

Running the Project

The current development setup has separate Docker Compose files for the dashboard and Airflow.

From the dashboard directory:

cd hospital_analytics
docker compose up --build

From the Airflow directory, in a separate terminal:

cd airflow
docker compose up --build -d

Snowflake connection settings must be configured locally. Do not commit passwords, access tokens, or other secrets to GitHub.

Validation

Before submission:

- Confirm that the dbt models build successfully.
- Confirm that all required dbt tests pass.
- Confirm that the Airflow DAG completes successfully.
- Confirm that the dashboard loads and its filters work.
- Capture the required screenshots of Snowflake, dbt tests, Airflow, Docker, and the dashboard.

Security

Credentials and secrets must remain outside version control. Use environment variables or an appropriately secured local secrets configuration.

Project Status

This README documents the current project structure and intended workflow. Verify the final deployment configuration and all required screenshots before submission.
