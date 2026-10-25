SELECT
    ID AS organization_id,
    NAME AS organization_name,
    ADDRESS AS organization_address,
    CITY AS organization_city,
    STATE AS organization_state,
    ZIP AS organization_zip,
    LAT AS latitude,
    LON AS longitude
FROM HOSPITAL_DB.RAW.ORGANIZATIONS
