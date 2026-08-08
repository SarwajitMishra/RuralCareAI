"""
Patient service for database operations.
"""

from sqlalchemy import select

from src.database.database import get_session
from src.database.models import Patient


class PatientService:

    @staticmethod
    def generate_patient_code():

        session = get_session()

        try:

            count = session.query(Patient).count()

            return f"PAT{count + 1:05d}"

        finally:

            session.close()

    @staticmethod
    def add_patient(**kwargs):

        session = get_session()

        try:

            patient = Patient(**kwargs)

            session.add(patient)

            session.commit()

            session.refresh(patient)

            return patient

        finally:

            session.close()

    @staticmethod
    def get_all_patients():

        session = get_session()

        try:

            patients = session.scalars(
                select(Patient).order_by(Patient.id.desc())
            ).all()

            return patients

        finally:

            session.close()

    @staticmethod
    def get_patient(patient_id):

        session = get_session()

        try:

            return session.get(Patient, patient_id)

        finally:

            session.close()