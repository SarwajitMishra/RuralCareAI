"""
Initializes the SQLite database.
Creates all tables and inserts a default administrator.
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

    finally:

        session.close()


if __name__ == "__main__":

    initialize_database()