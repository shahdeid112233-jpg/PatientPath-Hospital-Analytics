{{ config(materialized='table') }}

SELECT
    procedure_code,
    procedure_description,

    COUNT(*) AS procedure_count,

    AVG(procedure_base_cost) AS average_procedure_cost,

    SUM(procedure_base_cost) AS total_procedure_cost

FROM {{ ref('fct_procedures') }}

GROUP BY
    procedure_code,
    procedure_description
