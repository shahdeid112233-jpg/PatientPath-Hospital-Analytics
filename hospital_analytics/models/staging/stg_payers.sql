SELECT
    ID AS payer_id,
    NAME AS payer_name,
    ADDRESS AS payer_address,
    CITY AS payer_city,
    STATE_HEADQUARTERED AS state_headquartered,
    ZIP AS payer_zip,
    PHONE AS payer_phone
FROM HOSPITAL_DB.RAW.PAYERS
