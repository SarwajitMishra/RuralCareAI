"""
Consultation Database Model

This module defines the Consultation table used to store
patient consultations and AI prediction results.

Author: Sarwajit Kumar Mishra
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from src.database.models.base import Base


class Consultation(Base):
    """
    Represents a patient consultation.

    Each consultation belongs to exactly one patient and
    stores the AI prediction generated during diagnosis.
    """

    __tablename__ = "consultations"

    consultation_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True,
    )

    # Stored as JSON string
    symptoms = Column(
        Text,
        nullable=False,
    )

    predicted_disease = Column(
        String(150),
        nullable=False,
    )

    confidence = Column(
        Float,
        nullable=False,
    )

    image_path = Column(
        String(500),
        nullable=True,
    )

    image_prediction = Column(
        String(150),
        nullable=True,
    )

    image_confidence = Column(
        Float,
        nullable=True,
    )

    voice_transcript = Column(
        Text,
        nullable=True,
    )

    fusion_prediction = Column(
        String(150),
        nullable=True,
    )

    fusion_confidence = Column(
        Float,
        nullable=True,
    )

    risk_level = Column(
        String(20),
        nullable=False,
        default="Medium",
    )

    recommendation = Column(
        Text,
        nullable=True,
    )

    doctor_notes = Column(
        Text,
        nullable=True,
    )

    consultation_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    patient = relationship(
        "Patient",
        back_populates="consultations",
    )

    def __repr__(self):
        return (
            f"<Consultation("
            f"id={self.consultation_id}, "
            f"patient_id={self.patient_id}, "
            f"disease='{self.predicted_disease}', "
            f"confidence={self.confidence:.2f}%)>"
        )