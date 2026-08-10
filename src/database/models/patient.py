"""
Patient model for RuralCareAI.
"""

from datetime import date

from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.models.base import Base, TimestampMixin


class Patient(Base, TimestampMixin):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    patient_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    blood_group: Mapped[str] = mapped_column(
        String(10),
        nullable=True,
    )

    mobile_number: Mapped[str] = mapped_column(
        String(15),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    village: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    district: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    pincode: Mapped[str] = mapped_column(
        String(10),
        nullable=True,
    )

    height_cm: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    weight_kg: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    date_of_registration: Mapped[date] = mapped_column(
        Date,
        default=date.today,
        nullable=False,
    )

    remarks: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
    )

    chronic_conditions: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
    )

    consultations = relationship(
        "Consultation",
        back_populates="patient",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<Patient("
            f"id={self.id}, "
            f"patient_code='{self.patient_code}', "
            f"name='{self.full_name}')>"
        )