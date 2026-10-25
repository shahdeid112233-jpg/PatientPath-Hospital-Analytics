{{ config(materialized='table') }}

WITH ordered_encounters AS (
    SELECT
        encounter_id,
        patient_id,
        encounter_start,
        encounter_stop,
        encounter_class,

        LAG(encounter_id) OVER (
            PARTITION BY patient_id
            ORDER BY encounter_start, encounter_id
        ) AS previous_encounter_id,

        LAG(encounter_stop) OVER (
            PARTITION BY patient_id
            ORDER BY encounter_start, encounter_id
        ) AS previous_encounter_stop

    FROM {{ ref('fct_encounters') }}
    WHERE encounter_start IS NOT NULL
),

readmission_flags AS (
    SELECT
        *,
        CASE
            WHEN previous_encounter_id IS NOT NULL
             AND previous_encounter_stop IS NOT NULL
             AND encounter_start >= previous_encounter_stop
             AND encounter_start <= DATEADD(
                 day, 30, previous_encounter_stop
             )
            THEN 1
            ELSE 0
        END AS readmission_within_30_days

    FROM ordered_encounters
)

SELECT
    patient_id,
    encounter_id,
    encounter_start,
    encounter_stop,
    encounter_class,
    previous_encounter_id,
    previous_encounter_stop,
    readmission_within_30_days

FROM readmission_flags
