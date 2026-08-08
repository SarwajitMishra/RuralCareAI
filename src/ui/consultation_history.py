"""
Consultation History UI

Displays all patient consultations.
"""

import json

import pandas as pd
import streamlit as st

from src.services.patient_service import PatientService
from src.services.consultation_service import ConsultationService


patient_service = PatientService()
consultation_service = ConsultationService()


def show_consultation_history():

    st.title("📜 Consultation History")

    st.caption(
        "View previous consultations and AI diagnosis history."
    )

    patients = patient_service.get_all_patients()

    if not patients:

        st.info("No patients available.")

        return

    patient_lookup = {

        f"{patient.patient_code} - {patient.full_name}": patient.id

        for patient in patients

    }

    selected = st.selectbox(

        "Select Patient",

        list(patient_lookup.keys())

    )

    patient_id = patient_lookup[selected]

    history = consultation_service.get_patient_history(patient_id)

    if not history:

        st.warning(
            "No consultation history available."
        )

        return

    st.metric(

        "Total Consultations",

        len(history)

    )

    st.divider()

    records = []

    for consultation in history:

        symptoms = json.loads(
            consultation.symptoms
        )

        records.append({

            "Date":
                consultation.consultation_date.strftime(
                    "%d-%m-%Y %H:%M"
                ),

            "Disease":
                consultation.predicted_disease,

            "Confidence":
                f"{consultation.confidence:.2f}%",

            "Risk":
                consultation.risk_level,

            "Symptoms":
                ", ".join(symptoms),

            "Doctor Notes":
                consultation.doctor_notes,

        })

    df = pd.DataFrame(records)

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True,

    )

    st.divider()

    st.subheader("Consultation Details")

    consultation_index = st.selectbox(

        "Select Consultation",

        range(len(history)),

        format_func=lambda x:
        history[x].consultation_date.strftime(
            "%d-%m-%Y %H:%M"
        ),

    )

    consultation = history[consultation_index]

    symptoms = json.loads(
        consultation.symptoms
    )

    left, right = st.columns(2)

    with left:

        st.text_input(

            "Predicted Disease",

            consultation.predicted_disease,

            disabled=True,

        )

        st.text_input(

            "Confidence",

            f"{consultation.confidence:.2f}%",

            disabled=True,

        )

        st.text_input(

            "Risk Level",

            consultation.risk_level,

            disabled=True,

        )

    with right:

        st.text_input(

            "Consultation Date",

            consultation.consultation_date.strftime(
                "%d-%m-%Y %H:%M"
            ),

            disabled=True,

        )

        st.text_input(

            "Recommendation",

            consultation.recommendation,

            disabled=True,

        )

    st.subheader("Symptoms")

    symptom_df = pd.DataFrame({

        "Symptoms": symptoms

    })

    st.dataframe(

        symptom_df,

        use_container_width=True,

        hide_index=True,

    )

    st.subheader("Doctor Notes")

    st.text_area(

        "",

        consultation.doctor_notes,

        height=150,

        disabled=True,

    )