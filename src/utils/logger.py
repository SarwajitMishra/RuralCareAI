"""
Application logging configuration.

This module provides centralized logging for the RuralCare AI application.

Features
--------
- Console logging
- Rotating file logging
- Automatic log directory creation
- Singleton logger instance
- Configurable log level
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from src.config import config, create_required_directories

LOGGER_NAME = "ruralcare"


def configure_logging() -> logging.Logger:
    """
    Configure and return the application logger.

    Returns
    -------
    logging.Logger
        Configured application logger.
    """

    # ------------------------------------------------------------------
    # Ensure required directories exist before creating log file
    # ------------------------------------------------------------------
    create_required_directories()

    logger = logging.getLogger(LOGGER_NAME)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(
        getattr(
            logging,
            config.log_level.upper(),
            logging.INFO,
        )
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ------------------------------------------------------------------
    # Console Handler
    # ------------------------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logger.level)
    console_handler.setFormatter(formatter)

    # ------------------------------------------------------------------
    # Rotating File Handler
    # ------------------------------------------------------------------

    file_handler = RotatingFileHandler(
        filename=config.log_file,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setLevel(logger.level)
    file_handler.setFormatter(formatter)

    # ------------------------------------------------------------------
    # Register Handlers
    # ------------------------------------------------------------------

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    logger.info("-" * 70)
    logger.info("%s v%s", config.app_name, config.app_version)
    logger.info("Logging initialized successfully.")
    logger.info("Log file: %s", config.log_file)
    logger.info("-" * 70)

    return logger


logger = configure_logging()