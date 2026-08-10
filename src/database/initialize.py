"""
Initializes the SQLite database.
Creates all tables and inserts default demo accounts (an
administrator and a frontline healthcare worker).
"""

from sqlalchemy import select

from src.database.database import create_database
from src.database.database import get_session

from src.database.models import User
from src.auth.password import hash_password


def initialize_database():

    create_database()

    session = get_session()

    try:

        admin = session.scalar(
            select(User).where(User.username == "admin")
        )

        if admin is None:

            admin = User(
                username="admin",
                full_name="System Administrator",
                password=hash_password("admin123"),
                role="Administrator",
                is_active=True,
            )

            session.add(admin)
            session.commit()

            print("[OK] Default administrator created.")

        else:

            print("[OK] Administrator already exists.")

        # Matches the "USER AUTHENTICATION" mockup in the viva deck
        # (System Implementation slide), which demos login as a
        # frontline healthcare worker rather than an admin.
        health_worker = session.scalar(
            select(User).where(User.username == "HealthcareWorker1")
        )

        if health_worker is None:

            health_worker = User(
                username="HealthcareWorker1",
                full_name="Healthcare Worker",
                password=hash_password("healthworker123"),
                role="Health Worker",
                is_active=True,
            )

            session.add(health_worker)
            session.commit()

            print("[OK] Default health worker account created.")

        else:

            print("[OK] Health worker account already exists.")

    finally:

        session.close()


if __name__ == "__main__":

    initialize_database()