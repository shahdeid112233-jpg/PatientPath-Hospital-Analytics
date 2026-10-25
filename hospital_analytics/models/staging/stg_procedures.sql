SELECT
    "START" AS procedure_start,
    "STOP" AS procedure_stop,
    PATIENT AS patient_id,
    ENCOUNTER AS encounter_id,
    CODE AS procedure_code,
    DESCRIPTION AS procedure_description,
    BASE_COST AS base_cost,
    REASONCODE AS reason_code,
    REASONDESCRIPTION AS reason_description
FROM HOSPITAL_DB.RAW.PROCEDURES
