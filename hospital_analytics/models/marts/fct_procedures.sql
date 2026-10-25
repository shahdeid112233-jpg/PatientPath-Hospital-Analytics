{{ config(materialized='table') }}

SELECT
    patient_id,
    encounter_id,
    procedure_start,
    procedure_stop,
    procedure_code,
    procedure_description,
    procedure_base_cost,
    encounter_class,
    encounter_start,
    encounter_total_claim_cost,
    payer_coverage
FROM {{ ref('int_procedures_enriched') }}
