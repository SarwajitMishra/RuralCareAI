"""
Database configuration for RuralCareAI.
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base


# ------------------------------------------------------------------
# Database Path
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "data"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_FILE = DATABASE_DIR / "ruralcareai.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE}"


# ------------------------------------------------------------------
# SQLAlchemy Engine
# ------------------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# ------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------

def get_session():
    """
    Returns a new SQLAlchemy session.
    """

    return SessionLocal()


def create_database():
    """
    Creates all database tables.
    """

    Base.metadata.create_all(bind=engine)