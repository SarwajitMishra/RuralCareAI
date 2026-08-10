"""
Patient List UI
"""

import pandas as pd
import streamlit as st

from src.services.patient_service import PatientService
from src.ui.patient_registration import BLOOD_GROUPS, CHRONIC_CONDITIONS, GENDERS


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

    # Widget keys are tied to patient.id so switching the selected
    # patient always shows that patient's own values, instead of
    # Streamlit retaining stale input from whichever patient was
    # edited previously (widgets are keyed by identity, not by the
    # `value=`/default passed to them).

    with st.form(f"edit_patient_form_{patient.id}"):

        c1, c2 = st.columns(2)

        with c1:

            st.text_input(
                "Patient ID",
                patient.patient_code,
                disabled=True,
            )

            full_name = st.text_input(
                "Name",
                patient.full_name,
                key=f"edit_name_{patient.id}",
            )

            gender = st.selectbox(
                "Gender",
                GENDERS,
                index=GENDERS.index(patient.gender) if patient.gender in GENDERS else 0,
                key=f"edit_gender_{patient.id}",
            )

            blood_group = st.selectbox(
                "Blood Group",
                BLOOD_GROUPS,
                index=BLOOD_GROUPS.index(patient.blood_group) if patient.blood_group in BLOOD_GROUPS else 0,
                key=f"edit_blood_group_{patient.id}",
            )

            mobile = st.text_input(
                "Mobile",
                patient.mobile_number or "",
                key=f"edit_mobile_{patient.id}",
            )

        with c2:

            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=patient.age,
                key=f"edit_age_{patient.id}",
            )

            village = st.text_input(
                "Village",
                patient.village or "",
                key=f"edit_village_{patient.id}",
            )

            district = st.text_input(
                "District",
                patient.district or "",
                key=f"edit_district_{patient.id}",
            )

            state = st.text_input(
                "State",
                patient.state or "",
                key=f"edit_state_{patient.id}",
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=0,
                max_value=300,
                value=patient.weight_kg or 0,
                key=f"edit_weight_{patient.id}",
            )

        st.divider()

        st.markdown("**Medical History**")

        existing_conditions = (
            [c.strip() for c in patient.chronic_conditions.split(",") if c.strip()]
            if patient.chronic_conditions else []
        )

        chronic_conditions = st.multiselect(
            "Known Chronic Conditions",
            CHRONIC_CONDITIONS,
            default=[c for c in existing_conditions if c in CHRONIC_CONDITIONS],
            key=f"edit_chronic_conditions_{patient.id}",
        )

        remarks = st.text_area(
            "Other Medical History / Remarks",
            patient.remarks or "",
            height=120,
            key=f"edit_remarks_{patient.id}",
        )

        save = st.form_submit_button(
            "💾 Save Changes",
            type="primary",
        )

    if save:

        if not full_name.strip():

            st.error("Patient name is required.")

        else:

            try:

                PatientService.update_patient(

                    patient.id,

                    full_name=full_name.strip(),

                    age=int(age),

                    gender=gender,

                    blood_group=blood_group if blood_group else None,

                    mobile_number=mobile.strip(),

                    village=village.strip(),

                    district=district.strip(),

                    state=state.strip(),

                    weight_kg=int(weight),

                    remarks=remarks.strip(),

                    chronic_conditions=", ".join(chronic_conditions) if chronic_conditions else None,

                )

                st.success("✅ Patient details updated successfully.")

                st.rerun()

            except Exception as ex:

                st.exception(ex)