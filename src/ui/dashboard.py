"""
Dashboard UI

RuralCareAI Dashboard
"""

from collections import Counter

import pandas as pd
import streamlit as st
import json
from collections import Counter

from src.services.patient_service import PatientService
from src.services.consultation_service import ConsultationService

patient_service = PatientService()
consultation_service = ConsultationService()


def show_dashboard():

    st.title("🏥 RuralCareAI Dashboard")

    st.caption(
        "AI-Based Rural Healthcare Triage Assistant"
    )

    patients = patient_service.get_all_patients()

    total_patients = len(patients)

    consultations = []

    for patient in patients:

        consultations.extend(

            consultation_service.get_patient_history(
                patient.id
            )

        )

    total_consultations = len(consultations)

    total_predictions = total_consultations

    high_risk = len(
        [
            c
            for c in consultations
            if c.risk_level in ("High", "Critical")
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👥 Patients",
        total_patients,
    )

    c2.metric(
        "🩺 Consultations",
        total_consultations,
    )

    c3.metric(
        "🤖 Predictions",
        total_predictions,
    )

    c4.metric(
        "🚨 High Risk",
        high_risk,
    )

    st.divider()
    # ---------------------------------------------------------
    # Disease Distribution
    # ---------------------------------------------------------

    st.subheader("📊 Disease Distribution")

    if consultations:

        disease_df = pd.DataFrame([
            {
                "Disease": c.predicted_disease,
                "Count": 1,
            }
            for c in consultations
        ])

        disease_df = (
            disease_df.groupby("Disease")
            .count()
            .reset_index()
            .sort_values("Count", ascending=False)
        )

        tab1, tab2 = st.tabs(["Bar Chart", "Table"])

        with tab1:
            st.bar_chart(disease_df.set_index("Disease"))

        with tab2:
            st.dataframe(
                disease_df,
                use_container_width=True,
                hide_index=True,
            )

        st.subheader("🚨 Risk Distribution")

        risk_df = pd.DataFrame([
            {
                "Risk": c.risk_level,
                "Count": 1,
            }
            for c in consultations
        ])

        risk_df = (
            risk_df.groupby("Risk")
            .count()
            .reset_index()
        )

        st.bar_chart(risk_df.set_index("Risk"))

        st.subheader("🤒 Top Reported Symptoms")

        counter = Counter()

        for consultation in consultations:
            symptoms = json.loads(consultation.symptoms)

            counter.update(symptoms)

        symptom_df = pd.DataFrame({
            "Symptom": list(counter.keys()),
            "Frequency": list(counter.values())
        })

        symptom_df = symptom_df.sort_values(
            "Frequency",
            ascending=False,
        ).head(10)

        st.bar_chart(
            symptom_df.set_index("Symptom")
        )

    else:

        st.info("No consultation data available.")

    st.subheader("🚨 High Risk Patients")

    high_cases = [

        c

        for c in consultations

        if c.risk_level in ("High", "Critical")

    ]

    if high_cases:

        rows = []

        for consultation in high_cases:

            rows.append({

                "Patient":
                    consultation.patient.full_name,

                "Disease":
                    consultation.predicted_disease,

                "Risk":
                    consultation.risk_level,

                "Date":
                    consultation.consultation_date.strftime(
                        "%d-%m-%Y"
                    )

            })

        st.dataframe(

            pd.DataFrame(rows),

            use_container_width=True,

            hide_index=True,

        )

    else:

        st.success(
            "No high-risk patients currently."
        )
