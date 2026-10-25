SELECT
    p.patient_id,
    p.encounter_id,
    p.procedure_start,
    p.procedure_stop,
    p.procedure_code,
    p.procedure_description,
    p.base_cost AS procedure_base_cost,

    e.encounter_class,
    e.encounter_start,
    e.total_claim_cost AS encounter_total_claim_cost,
    e.payer_coverage

FROM {{ ref('stg_procedures') }} AS p

LEFT JOIN {{ ref('stg_encounters') }} AS e
    ON p.encounter_id = e.encounter_id
