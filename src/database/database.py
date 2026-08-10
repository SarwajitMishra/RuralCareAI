"""
Database configuration for RuralCareAI.
"""

from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, Consultation, Patient


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
    Creates all database tables and applies lightweight column
    migrations for existing databases (Base.metadata.create_all only
    creates missing tables, it does not alter existing ones).
    """

    Base.metadata.create_all(bind=engine)

    _migrate_schema()


def _migrate_schema():
    """
    Reconciles an already-existing SQLite database file with the
    current ORM model (Base.metadata.create_all only creates missing
    tables, it never alters existing ones).

    Older copies of ruralcareai.db may hold a "consultations" table
    from an earlier iteration of the model (different column names,
    e.g. confidence_score/severity instead of confidence/risk_level,
    with several current columns missing entirely). A single ADD
    COLUMN cannot fix that kind of drift, so when the mismatch is
    more than the known additive column and the table holds no rows,
    it is safely rebuilt from the current model instead.
    """

    inspector = inspect(engine)

    if "consultations" in inspector.get_table_names():
        _migrate_consultations_table(inspector)

    if "patients" in inspector.get_table_names():
        _migrate_patients_table(inspector)


def _migrate_consultations_table(inspector):

    existing_columns = {
        column["name"] for column in inspector.get_columns("consultations")
    }

    expected_columns = {column.name for column in Consultation.__table__.columns}

    missing_columns = expected_columns - existing_columns

    if not missing_columns:
        return

    if missing_columns == {"ai_summary"}:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE consultations ADD COLUMN ai_summary TEXT")
            )
        return

    with engine.connect() as connection:
        row_count = connection.execute(
            text("SELECT COUNT(*) FROM consultations")
        ).scalar()

    if row_count == 0:
        Consultation.__table__.drop(bind=engine)
        Consultation.__table__.create(bind=engine)
    else:
        raise RuntimeError(
            "The 'consultations' table schema is out of date "
            f"(missing columns: {sorted(missing_columns)}) and already "
            "contains data, so it cannot be rebuilt automatically. "
            "A manual migration is required."
        )


def _migrate_patients_table(inspector):

    existing_columns = {
        column["name"] for column in inspector.get_columns("patients")
    }

    expected_columns = {column.name for column in Patient.__table__.columns}

    missing_columns = expected_columns - existing_columns

    if not missing_columns:
        return

    if missing_columns == {"chronic_conditions"}:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE patients ADD COLUMN chronic_conditions VARCHAR(500)")
            )
        return

    with engine.connect() as connection:
        row_count = connection.execute(
            text("SELECT COUNT(*) FROM patients")
        ).scalar()

    if row_count == 0:
        Patient.__table__.drop(bind=engine)
        Patient.__table__.create(bind=engine)
    else:
        raise RuntimeError(
            "The 'patients' table schema is out of date "
            f"(missing columns: {sorted(missing_columns)}) and already "
            "contains data, so it cannot be rebuilt automatically. "
            "A manual migration is required."
        )