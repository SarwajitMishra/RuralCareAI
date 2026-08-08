"""
Patient List UI
"""

import pandas as pd
import streamlit as st

from src.services.patient_service import PatientService


def show_patient_list():

    st.title("📋 Patient List")
    st.caption("Search and manage registered patients")

    patients = PatientService.get_all_patients()

    if not patients:
        st.info("No patients registered yet.")
        return

    search = st.text_input(
        "🔍 Search by Patient ID, Name or Mobile"
    ).strip().lower()

    records = []

    for patient in patients:

        row = {
            "ID": patient.id,
            "Patient ID": patient.patient_code,
            "Name": patient.full_name,
            "Age": patient.age,
            "Gender": patient.gender,
            "Blood Group": patient.blood_group,
            "Mobile": patient.mobile_number,
            "Village": patient.village,
            "District": patient.district,
            "State": patient.state,
            "Height": patient.height_cm,
            "Weight": patient.weight_kg,
            "Remarks": patient.remarks,
        }

        records.append(row)

    df = pd.DataFrame(records)

    if search:

        mask = (
            df["Patient ID"].astype(str).str.lower().str.contains(search)
            | df["Name"].astype(str).str.lower().str.contains(search)
            | df["Mobile"].astype(str).str.lower().str.contains(search)
        )

        df = df[mask]

    st.metric(
        "Total Patients",
        len(df),
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Patient Details")

    patient_ids = df["Patient ID"].tolist()

    selected_patient = st.selectbox(
        "Select Patient",
        patient_ids,
    )

    patient = next(
        p for p in patients if p.patient_code == selected_patient
    )

    c1, c2 = st.columns(2)

    with c1:

        st.text_input(
            "Patient ID",
            patient.patient_code,
            disabled=True,
        )

        st.text_input(
            "Name",
            patient.full_name,
            disabled=True,
        )

        st.text_input(
            "Gender",
            patient.gender,
            disabled=True,
        )

        st.text_input(
            "Blood Group",
            patient.blood_group,
            disabled=True,
        )

        st.text_input(
            "Mobile",
            patient.mobile_number,
            disabled=True,
        )

    with c2:

        st.text_input(
            "Age",
            patient.age,
            disabled=True,
        )

        st.text_input(
            "Village",
            patient.village,
            disabled=True,
        )

        st.text_input(
            "District",
            patient.district,
            disabled=True,
        )

        st.text_input(
            "State",
            patient.state,
            disabled=True,
        )

        st.text_input(
            "Weight (kg)",
            patient.weight_kg,
            disabled=True,
        )

    st.text_area(
        "Remarks",
        patient.remarks,
        height=120,
        disabled=True,
    )