"""
Patient Registration UI
"""

from datetime import date
import re

import streamlit as st

from src.services.patient_service import PatientService


BLOOD_GROUPS = [
    "",
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-",
]

GENDERS = [
    "Male",
    "Female",
    "Other",
]


def _is_valid_email(email: str) -> bool:
    if not email:
        return True

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def _is_valid_mobile(mobile: str) -> bool:
    if not mobile:
        return True

    return mobile.isdigit() and len(mobile) == 10


def show_patient_registration():

    st.title("🩺 Patient Registration")
    st.caption("Register a new patient into RuralCareAI")

    patient_code = PatientService.generate_patient_code()

    with st.form("patient_registration_form", clear_on_submit=True):

        st.subheader("Basic Information")

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(
                "Patient ID",
                value=patient_code,
                disabled=True,
            )

            full_name = st.text_input(
                "Full Name *"
            )

            age = st.number_input(
                "Age *",
                min_value=0,
                max_value=120,
                value=25,
            )

            gender = st.selectbox(
                "Gender *",
                GENDERS,
            )

            blood_group = st.selectbox(
                "Blood Group",
                BLOOD_GROUPS,
            )

            mobile = st.text_input(
                "Mobile Number"
            )

            email = st.text_input(
                "Email"
            )

        with col2:

            village = st.text_input(
                "Village"
            )

            district = st.text_input(
                "District"
            )

            state = st.text_input(
                "State"
            )

            pincode = st.text_input(
                "Pincode"
            )

            height = st.number_input(
                "Height (cm)",
                min_value=0,
                max_value=250,
                value=170,
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=0,
                max_value=300,
                value=70,
            )

        remarks = st.text_area(
            "Remarks",
            height=120,
        )

        st.divider()

        col_save, col_space = st.columns([1, 3])

        save = col_save.form_submit_button(
            "💾 Register Patient",
            use_container_width=True,
        )

    if not save:
        return

    # ---------------- Validation ----------------

    if not full_name.strip():
        st.error("Patient name is required.")
        return

    if age <= 0:
        st.error("Age must be greater than zero.")
        return

    if not _is_valid_mobile(mobile):
        st.error("Invalid mobile number.")
        return

    if not _is_valid_email(email):
        st.error("Invalid email address.")
        return

    try:

        PatientService.add_patient(

            patient_code=patient_code,

            full_name=full_name.strip(),

            age=int(age),

            gender=gender,

            blood_group=blood_group if blood_group else None,

            mobile_number=mobile.strip(),

            email=email.strip(),

            village=village.strip(),

            district=district.strip(),

            state=state.strip(),

            pincode=pincode.strip(),

            height_cm=int(height),

            weight_kg=int(weight),

            date_of_registration=date.today(),

            remarks=remarks.strip(),
        )

        st.success("✅ Patient registered successfully.")

        st.balloons()

    except Exception as ex:

        st.exception(ex)