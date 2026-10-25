{{ config(materialized='table') }}

SELECT
    encounter_year,
    encounter_quarter,
    encounter_class,

    COUNT(*) AS total_encounters,

    COUNT(DISTINCT patient_id) AS unique_patients,

    SUM(total_claim_cost) AS total_claim_cost,

    AVG(total_claim_cost) AS average_claim_cost,

    SUM(payer_coverage) AS total_payer_coverage,

    COUNT_IF(
        COALESCE(payer_coverage, 0) = 0
    ) AS zero_coverage_encounters,

    AVG(encounter_duration_hours) AS average_duration_hours,

    COUNT_IF(
        encounter_duration_hours > 24
    ) AS encounters_over_24_hours

FROM {{ ref('fct_encounters') }}

GROUP BY
    encounter_year,
    encounter_quarter,
    encounter_class
