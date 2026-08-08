"""
Authentication utilities.
"""

from sqlalchemy import select

from src.database.database import get_session
from src.database.models import User
from src.auth.password import verify_password


def authenticate(username: str, password: str):

    session = get_session()

    try:

        user = session.scalar(
            select(User).where(
                User.username == username,
                User.is_active == True,
            )
        )

        if user is None:
            return None

        if verify_password(password, user.password):
            return user

        return None

    finally:

        session.close()