{{ config(materialized='table') }}

SELECT
    patient_id,
    gender,
    race,
    ethnicity,
    birth_date,
    CASE
        WHEN birth_date IS NULL THEN 'Unknown'
        WHEN DATEDIFF(year, birth_date, CURRENT_DATE()) < 18 THEN 'Under 18'
        WHEN DATEDIFF(year, birth_date, CURRENT_DATE()) < 35 THEN '18-34'
        WHEN DATEDIFF(year, birth_date, CURRENT_DATE()) < 50 THEN '35-49'
        WHEN DATEDIFF(year, birth_date, CURRENT_DATE()) < 65 THEN '50-64'
        ELSE '65+'
    END AS age_group
FROM {{ ref('stg_patients') }}
