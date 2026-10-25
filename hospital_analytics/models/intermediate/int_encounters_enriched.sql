SELECT
    e.encounter_id,
    e.patient_id,
    e.organization_id,
    e.payer_id,
    e.encounter_start,
    e.encounter_stop,
    e.encounter_class,
    e.encounter_code,
    e.encounter_description,
    e.base_encounter_cost,
    e.total_claim_cost,
    e.payer_coverage,
    e.reason_code,
    e.reason_description,

    p.gender,
    p.race,
    p.ethnicity,
    p.birth_date,

    DATEDIFF(
        year,
        p.birth_date,
        e.encounter_start
    )
    - CASE
        WHEN DATEADD(
            year,
            DATEDIFF(year, p.birth_date, e.encounter_start),
            p.birth_date
        ) > e.encounter_start
        THEN 1
        ELSE 0
      END AS patient_age_at_encounter,

    DATEDIFF(
        second,
        e.encounter_start,
        e.encounter_stop
    ) / 3600.0 AS encounter_duration_hours

FROM {{ ref('stg_encounters') }} AS e

LEFT JOIN {{ ref('stg_patients') }} AS p
    ON e.patient_id = p.patient_id
