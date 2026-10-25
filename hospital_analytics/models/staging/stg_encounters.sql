SELECT
    ID AS encounter_id,
    "START " AS encounter_start,
    STOP AS encounter_stop,
    PATIENT AS patient_id,
    ORGANIZATION AS organization_id,
    PAYER AS payer_id,
    ENCOUNTERCLASS AS encounter_class,
    CODE AS encounter_code,
    DESCRIPTION AS encounter_description,
    BASE_ENCOUNTER_COST AS base_encounter_cost,
    TOTAL_CLAIM_COST AS total_claim_cost,
    PAYER_COVERAGE AS payer_coverage,
    REASONCODE AS reason_code,
    REASONDESCRIPTION AS reason_description
FROM HOSPITAL_DB.RAW.ENCOUNTERS
