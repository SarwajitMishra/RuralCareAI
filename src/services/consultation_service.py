"""
Consultation Service

Business logic for patient consultations.

Responsibilities:
- Predict disease
- Calculate risk level
- Generate recommendation
- Save consultation
- Retrieve consultation history

Author: Sarwajit Kumar Mishra
"""

import json

from sqlalchemy.orm import joinedload

from src.database.database import get_session
from src.database.models.consultation import Consultation
from src.ml.predictor import DiseasePredictor


class ConsultationService:

    def __init__(self):
        self.predictor = DiseasePredictor()

    # ---------------------------------------------------------
    # Prediction
    # ---------------------------------------------------------

    def predict(self, symptoms: list[str]) -> dict:
        """
        Predict disease using the trained ML model.
        """

        result = self.predictor.predict(symptoms)

        disease = result["predicted_disease"]

        result["risk_level"] = self._risk_level(disease)
        result["recommendation"] = self._recommendation(disease)

        return result

    # ---------------------------------------------------------
    # Save Consultation
    # ---------------------------------------------------------

    def save_consultation(
        self,
            patient_id: int,
            symptoms: list[str],
            prediction_result: dict,
            doctor_notes: str = "",
            image_path: str | None = None,
            image_prediction: str | None = None,
            image_confidence: float | None = None,
            voice_transcript: str | None = None,
            fusion_prediction: str | None = None,
            fusion_confidence: float | None = None
    ) -> Consultation:
        """
        Save consultation into the database.
        """

        session = get_session()

        try:

            consultation = Consultation(
                patient_id=patient_id,
                symptoms=json.dumps(symptoms),
                predicted_disease=prediction_result["predicted_disease"],
                confidence=prediction_result["confidence"],
                risk_level=prediction_result["risk_level"],
                recommendation=prediction_result["recommendation"],
                doctor_notes=doctor_notes,
                image_path=image_path,
                image_prediction=image_prediction,
                image_confidence=image_confidence,
                voice_transcript=voice_transcript,
                fusion_prediction=fusion_prediction,
                fusion_confidence=fusion_confidence,
            )

            session.add(consultation)
            session.commit()
            session.refresh(consultation)

            return consultation

        finally:
            session.close()

    # ---------------------------------------------------------
    # History
    # ---------------------------------------------------------

    def get_patient_history(
        self,
        patient_id: int,
    ) -> list[Consultation]:
        """
        Return all consultations of a patient.
        """

        session = get_session()

        try:

            return (
                session.query(Consultation)
                .options(joinedload(Consultation.patient))
                .filter(
                    Consultation.patient_id == patient_id
                )
                .order_by(
                    Consultation.consultation_date.desc()
                )
                .all()
            )

        finally:
            session.close()

    # ---------------------------------------------------------
    # Latest Consultation
    # ---------------------------------------------------------

    def get_latest_consultation(
        self,
        patient_id: int,
    ):
        """
        Return latest consultation.
        """

        session = get_session()

        try:

            return (
                session.query(Consultation)
                .filter(
                    Consultation.patient_id == patient_id
                )
                .order_by(
                    Consultation.consultation_date.desc()
                )
                .first()
            )

        finally:
            session.close()

    # ---------------------------------------------------------
    # Risk Engine
    # ---------------------------------------------------------

    @staticmethod
    def _risk_level(disease: str) -> str:

        critical = {
            "Heart attack",
            "Paralysis (brain hemorrhage)",
        }

        high = {
            "Dengue",
            "Malaria",
            "Typhoid",
            "Tuberculosis",
            "Pneumonia",
            "Hepatitis B",
            "Hepatitis C",
            "Hepatitis D",
            "Hepatitis E",
        }

        medium = {
            "Diabetes ",
            "Hypertension ",
            "Bronchial Asthma",
            "Hypoglycemia",
        }

        if disease in critical:
            return "Critical"

        if disease in high:
            return "High"

        if disease in medium:
            return "Medium"

        return "Low"

    # ---------------------------------------------------------
    # Recommendation Engine
    # ---------------------------------------------------------

    @staticmethod
    def _recommendation(disease: str) -> str:

        risk = ConsultationService._risk_level(disease)

        recommendations = {
            "Critical":
                "Immediate referral to the nearest emergency hospital.",

            "High":
                "Refer to a physician or district hospital within 24 hours.",

            "Medium":
                "Clinical evaluation and follow-up recommended.",

            "Low":
                "Home care, medication as advised, and monitor symptoms.",
        }

        return recommendations[risk]