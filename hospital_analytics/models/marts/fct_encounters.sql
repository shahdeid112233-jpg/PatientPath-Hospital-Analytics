{{ config(materialized='table') }}

SELECT
    encounter_id,
    patient_id,
    organization_id,
    payer_id,
    encounter_start,
    encounter_stop,
    encounter_class,
    encounter_code,
    encounter_description,
    base_encounter_cost,
    total_claim_cost,
    payer_coverage,
    reason_code,
    reason_description,

    DATEDIFF(
        second,
        encounter_start,
        encounter_stop
    ) / 3600.0 AS encounter_duration_hours,

    YEAR(encounter_start) AS encounter_year,
    QUARTER(encounter_start) AS encounter_quarter

FROM {{ ref('int_encounters_enriched') }}
