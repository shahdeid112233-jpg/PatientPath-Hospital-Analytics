{{ config(materialized='table') }}

SELECT
    payer_id,
    payer_name,
    payer_city,
    state_headquartered
FROM {{ ref('stg_payers') }}
