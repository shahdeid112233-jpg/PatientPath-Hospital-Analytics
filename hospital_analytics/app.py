import streamlit as st
import snowflake.connector
import pandas as pd

st.set_page_config(
    page_title="Hospital Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("Hospital Analytics Dashboard")
st.caption("Hospital encounters, costs, procedures, and readmissions")


@st.cache_data(ttl=300)
def load_data(query):
    connection = snowflake.connector.connect(
        **dict(st.secrets["snowflake"])
    )
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    finally:
        cursor.close()
        connection.close()


try:
    encounters = load_data("""
        SELECT
            ENCOUNTER_ID,
            PATIENT_ID,
            ENCOUNTER_START,
            ENCOUNTER_YEAR,
            ENCOUNTER_QUARTER,
            ENCOUNTER_CLASS,
            TOTAL_CLAIM_COST,
            PAYER_COVERAGE,
            ENCOUNTER_DURATION_HOURS
        FROM HOSPITAL_DB.MARTS.FCT_ENCOUNTERS
    """)

    procedures = load_data("""
        SELECT
            PROCEDURE_CODE,
            PROCEDURE_DESCRIPTION,
            PROCEDURE_COUNT,
            AVERAGE_PROCEDURE_COST,
            TOTAL_PROCEDURE_COST
        FROM HOSPITAL_DB.MARTS.MART_PROCEDURE_SUMMARY
    """)
    procedures["PROCEDURE_COUNT"] = pd.to_numeric(
        procedures["PROCEDURE_COUNT"], errors="coerce"
    )
    procedures["AVERAGE_PROCEDURE_COST"] = pd.to_numeric(
        procedures["AVERAGE_PROCEDURE_COST"], errors="coerce"
    )
    procedures["TOTAL_PROCEDURE_COST"] = pd.to_numeric(
        procedures["TOTAL_PROCEDURE_COST"], errors="coerce"
    )
    payers = load_data("""
        SELECT
            p.PAYER_NAME,
            AVG(e.TOTAL_CLAIM_COST) AS AVERAGE_CLAIM_COST
        FROM HOSPITAL_DB.MARTS.FCT_ENCOUNTERS e
        LEFT JOIN HOSPITAL_DB.MARTS.DIM_PAYERS p
            ON e.PAYER_ID = p.PAYER_ID
        GROUP BY p.PAYER_NAME
        ORDER BY AVERAGE_CLAIM_COST DESC
    """)

    readmissions = load_data("""
        SELECT
            PATIENT_ID,
            ENCOUNTER_ID,
            READMISSION_WITHIN_30_DAYS
        FROM HOSPITAL_DB.MARTS.MART_READMISSIONS
    """)

    if encounters.empty:
        st.warning("No encounter data is available.")
        st.stop()

    encounters["ENCOUNTER_START"] = pd.to_datetime(
        encounters["ENCOUNTER_START"]
    )

    st.sidebar.header("Filters")

    years = sorted(
        encounters["ENCOUNTER_YEAR"].dropna().astype(int).unique()
    )
    selected_years = st.sidebar.multiselect(
        "Encounter year",
        years,
        default=years
    )

    classes = sorted(
        encounters["ENCOUNTER_CLASS"].dropna().unique().tolist()
    )
    selected_classes = st.sidebar.multiselect(
        "Encounter class",
        classes,
        default=classes
    )

    filtered = encounters[
        encounters["ENCOUNTER_YEAR"].isin(selected_years)
        & encounters["ENCOUNTER_CLASS"].isin(selected_classes)
    ].copy()

    # Main KPIs
    total_encounters = len(filtered)
    unique_patients = filtered["PATIENT_ID"].nunique()
    average_cost = filtered["TOTAL_CLAIM_COST"].mean()

    zero_coverage = (
        filtered["PAYER_COVERAGE"].fillna(0) == 0
    ).sum()

    zero_coverage_pct = (
        zero_coverage / total_encounters * 100
        if total_encounters else 0
    )

    long_encounters = (
        filtered["ENCOUNTER_DURATION_HOURS"] > 24
    ).sum()

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total Encounters", f"{total_encounters:,}")
    k2.metric("Unique Patients", f"{unique_patients:,}")
    k3.metric(
        "Average Claim Cost",
        f"${average_cost:,.2f}" if pd.notna(average_cost) else "N/A"
    )
    k4.metric("Zero Coverage", f"{zero_coverage_pct:.1f}%")

    st.divider()
    st.subheader("Encounter Trends")

    if not filtered.empty:
        yearly = (
            filtered.groupby("ENCOUNTER_YEAR", as_index=False)
            .agg(Total_Encounters=("ENCOUNTER_ID", "count"))
            .sort_values("ENCOUNTER_YEAR")
        )

        st.line_chart(
            yearly,
            x="ENCOUNTER_YEAR",
            y="Total_Encounters"
        )

        left, right = st.columns(2)

        with left:
            by_class = (
                filtered.groupby("ENCOUNTER_CLASS", as_index=False)
                .agg(Total_Encounters=("ENCOUNTER_ID", "count"))
                .sort_values("Total_Encounters", ascending=False)
            )

            st.subheader("Encounters by Class")
            st.bar_chart(
                by_class,
                x="ENCOUNTER_CLASS",
                y="Total_Encounters"
            )

        with right:
            quarterly = (
                filtered.groupby(
                    ["ENCOUNTER_YEAR", "ENCOUNTER_QUARTER"],
                    as_index=False
                )
                .agg(Unique_Patients=("PATIENT_ID", "nunique"))
                .sort_values(
                    ["ENCOUNTER_YEAR", "ENCOUNTER_QUARTER"]
                )
            )

            quarterly["Period"] = (
                quarterly["ENCOUNTER_YEAR"].astype(str)
                + " Q"
                + quarterly["ENCOUNTER_QUARTER"].astype(str)
            )

            st.subheader("Unique Patients by Quarter")
            st.bar_chart(
                quarterly,
                x="Period",
                y="Unique_Patients"
            )

    # Encounter duration
    st.divider()
    st.subheader("Encounter Duration")

    d1, d2 = st.columns(2)

    d1.metric(
        "Encounters Longer Than 24 Hours",
        f"{long_encounters:,}"
    )

    if not filtered.empty:
        duration_by_class = (
            filtered.groupby("ENCOUNTER_CLASS", as_index=False)
            .agg(
                Average_Duration_Hours=(
                    "ENCOUNTER_DURATION_HOURS", "mean"
                )
            )
        )

        with d2:
            st.metric(
                "Average Duration (Hours)",
                f"{filtered['ENCOUNTER_DURATION_HOURS'].mean():,.2f}"
                if pd.notna(
                    filtered["ENCOUNTER_DURATION_HOURS"].mean()
                )
                else "N/A"
            )

        st.bar_chart(
            duration_by_class,
            x="ENCOUNTER_CLASS",
            y="Average_Duration_Hours"
        )

    # Procedures
    st.divider()
    st.subheader("Procedure Analysis")

    left, right = st.columns(2)

    with left:
        st.write("Most Frequent Procedures")

        st.bar_chart(
            procedures.nlargest(10, "PROCEDURE_COUNT"),
            x="PROCEDURE_DESCRIPTION",
            y="PROCEDURE_COUNT"
        )

    with right:
        st.write("Procedures with Highest Average Cost")

        st.bar_chart(
            procedures.nlargest(10, "AVERAGE_PROCEDURE_COST"),
            x="PROCEDURE_DESCRIPTION",
            y="AVERAGE_PROCEDURE_COST"
        )

    st.subheader("Procedure Details")

    st.dataframe(
        procedures.sort_values(
            "PROCEDURE_COUNT", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    # Payer analysis
    st.divider()
    st.subheader("Average Claim Cost by Payer")

    st.bar_chart(
        payers,
        x="PAYER_NAME",
        y="AVERAGE_CLAIM_COST"
    )

    # Readmissions, filtered by selected encounter year and class
    st.divider()
    st.subheader("30-Day Readmissions")

    filtered_readmissions = readmissions[
        readmissions["ENCOUNTER_ID"].isin(
            filtered["ENCOUNTER_ID"]
        )
        & (
            readmissions["READMISSION_WITHIN_30_DAYS"] == 1
        )
    ].copy()

    readmission_count = len(filtered_readmissions)
    patients_readmitted = (
        filtered_readmissions["PATIENT_ID"].nunique()
    )

    r1, r2 = st.columns(2)

    r1.metric(
        "Readmission Encounters",
        f"{readmission_count:,}"
    )

    r2.metric(
        "Patients with Readmissions",
        f"{patients_readmitted:,}"
    )

    if not filtered_readmissions.empty:
        top_readmitted = (
            filtered_readmissions.groupby(
                "PATIENT_ID", as_index=False
            )
            .agg(
                Readmission_Count=("ENCOUNTER_ID", "count")
            )
            .sort_values(
                "Readmission_Count", ascending=False
            )
            .head(10)
        )

        st.write("Patients with the Most Readmissions")
        st.bar_chart(
            top_readmitted,
            x="PATIENT_ID",
            y="Readmission_Count"
        )
    else:
        st.info(
            "No readmissions were found for the selected filters."
        )

    st.caption(
        "Patient names, addresses, and exact locations are not displayed. "
        "Dashboard data is cached for 5 minutes."
    )

except Exception as error:
    st.error("Could not load dashboard data from Snowflake.")
    st.code(str(error))
    st.info(
        "Check the Snowflake connection, model names, and table permissions."
    )
