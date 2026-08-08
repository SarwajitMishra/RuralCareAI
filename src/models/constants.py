"""
Application-wide constants.

This module contains immutable constants used across the application.
Values that may change between deployments or environments should be
stored in the ApplicationSettings database table instead of here.
"""

from __future__ import annotations

from pathlib import Path

# -----------------------------------------------------------------------------
# Application Information
# -----------------------------------------------------------------------------

APP_NAME: str = "RuralCare AI"
APP_VERSION: str = "1.0.0"
APP_DESCRIPTION: str = (
    "AI-Based Rural Healthcare Triage Assistant using Multimodal Machine Learning"
)

# -----------------------------------------------------------------------------
# Directory Names
# -----------------------------------------------------------------------------

DATA_DIR_NAME: str = "data"
DATABASE_DIR_NAME: str = "database"
MODELS_DIR_NAME: str = "models"
UPLOADS_DIR_NAME: str = "uploads"
REPORTS_DIR_NAME: str = "reports"
LOGS_DIR_NAME: str = "logs"

# -----------------------------------------------------------------------------
# File Names
# -----------------------------------------------------------------------------

DATABASE_FILE_NAME: str = "ruralcare.db"
LOG_FILE_NAME: str = "ruralcare.log"

# -----------------------------------------------------------------------------
# Supported File Extensions
# -----------------------------------------------------------------------------

IMAGE_EXTENSIONS: tuple[str, ...] = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
)

AUDIO_EXTENSIONS: tuple[str, ...] = (
    ".wav",
    ".mp3",
    ".m4a",
)

DOCUMENT_EXTENSIONS: tuple[str, ...] = (
    ".pdf",
    ".docx",
    ".txt",
)

# -----------------------------------------------------------------------------
# Machine Learning
# -----------------------------------------------------------------------------

DEFAULT_RANDOM_STATE: int = 42
DEFAULT_TEST_SIZE: float = 0.20
DEFAULT_MODEL_DIRECTORY: str = MODELS_DIR_NAME

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

SQLITE_PREFIX: str = "sqlite:///"

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

DEFAULT_LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# -----------------------------------------------------------------------------
# Report Configuration
# -----------------------------------------------------------------------------

DEFAULT_REPORT_TITLE: str = (
    "RuralCare AI Consultation Report"
)

# -----------------------------------------------------------------------------
# Miscellaneous
# -----------------------------------------------------------------------------

DATE_FORMAT: str = "%Y-%m-%d"
DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

SUPPORTED_IMAGE_SIZE: tuple[int, int] = (512, 512)

# -----------------------------------------------------------------------------
# Project Root (resolved dynamically)
# -----------------------------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]