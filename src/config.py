"""
===============================================================================
Project : RuralCare AI
Author  : Sarwajit Kumar Mishra
BITS ID : 2024AA05184

Central configuration file for the entire application.

DO NOT hardcode file paths anywhere else in the project.
Always import paths from this file.
===============================================================================
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from src.models.constants import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    DATABASE_DIR_NAME,
    DATABASE_FILE_NAME,
    DATA_DIR_NAME,
    DEFAULT_LOG_LEVEL,
    LOGS_DIR_NAME,
    LOG_FILE_NAME,
    MODELS_DIR_NAME,
    PROJECT_ROOT,
    REPORTS_DIR_NAME,
    SQLITE_PREFIX,
    UPLOADS_DIR_NAME,
)

# Load environment variables from .env (if available)
load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Application configuration."""

    # ------------------------------------------------------------------
    # Application Information
    # ------------------------------------------------------------------

    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    app_description: str = APP_DESCRIPTION

    # ------------------------------------------------------------------
    # Project Paths
    # ------------------------------------------------------------------

    project_root: Path = PROJECT_ROOT

    data_dir: Path = PROJECT_ROOT / DATA_DIR_NAME
    database_dir: Path = PROJECT_ROOT / DATABASE_DIR_NAME
    models_dir: Path = PROJECT_ROOT / MODELS_DIR_NAME
    uploads_dir: Path = PROJECT_ROOT / UPLOADS_DIR_NAME
    reports_dir: Path = PROJECT_ROOT / REPORTS_DIR_NAME
    logs_dir: Path = PROJECT_ROOT / LOGS_DIR_NAME

    # ------------------------------------------------------------------
    # Files
    # ------------------------------------------------------------------

    database_file: Path = (
        PROJECT_ROOT
        / DATABASE_DIR_NAME
        / DATABASE_FILE_NAME
    )

    log_file: Path = (
        PROJECT_ROOT
        / LOGS_DIR_NAME
        / LOG_FILE_NAME
    )

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    log_level: str = os.getenv(
        "LOG_LEVEL",
        DEFAULT_LOG_LEVEL,
    )

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    database_url: str = os.getenv(
        "DATABASE_URL",
        f"{SQLITE_PREFIX}{database_file.as_posix()}",
    )

    # ------------------------------------------------------------------
    # AI / ML
    # ------------------------------------------------------------------

    random_seed: int = int(
        os.getenv("RANDOM_SEED", "42")
    )

    # ------------------------------------------------------------------
    # Debug
    # ------------------------------------------------------------------

    debug: bool = (
        os.getenv("DEBUG", "False").lower()
        == "true"
    )

    # ------------------------------------------------------------------
    # SQLAlchemy
    # ------------------------------------------------------------------

    echo_sql: bool = (
            os.getenv("SQL_ECHO", "False").lower() == "true"
    )

    pool_pre_ping: bool = True

    expire_on_commit: bool = False


# ----------------------------------------------------------------------
# Singleton Configuration
# ----------------------------------------------------------------------

config = AppConfig()


# ----------------------------------------------------------------------
# Directory Initialization
# ----------------------------------------------------------------------

def create_required_directories() -> None:
    """
    Create all required application directories.

    Safe to call multiple times.
    """

    directories = (
        config.data_dir,
        config.database_dir,
        config.models_dir,
        config.uploads_dir,
        config.reports_dir,
        config.logs_dir,
    )

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )