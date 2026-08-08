"""
Application enumerations.

This module contains all enumerations used across the RuralCare AI
application. Using enums instead of string literals improves type safety,
readability, validation, and maintainability.
"""

from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    """Base class for all string enumerations."""

    def __str__(self) -> str:
        return self.value


# ============================================================================
# User Management
# ============================================================================

class UserRole(StrEnum):
    """Application user roles."""

    ADMIN = "Admin"
    DOCTOR = "Doctor"
    HEALTH_WORKER = "Health Worker"
    DATA_ENTRY = "Data Entry"
    VIEWER = "Viewer"


class AccountStatus(StrEnum):
    """Status of a user account."""

    ACTIVE = "Active"
    INACTIVE = "Inactive"
    LOCKED = "Locked"
    ARCHIVED = "Archived"


# ============================================================================
# Patient
# ============================================================================

class Gender(StrEnum):
    """Patient gender."""

    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class BloodGroup(StrEnum):
    """Blood group."""

    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "Unknown"


class PatientStatus(StrEnum):
    """Patient record status."""

    ACTIVE = "Active"
    INACTIVE = "Inactive"
    ARCHIVED = "Archived"


# ============================================================================
# Consultation
# ============================================================================

class ConsultationStatus(StrEnum):
    """Consultation lifecycle."""

    DRAFT = "Draft"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Severity(StrEnum):
    """Clinical severity."""

    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"


class RiskLevel(StrEnum):
    """AI-generated patient risk level."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    EMERGENCY = "Emergency"


# ============================================================================
# Language
# ============================================================================

class Language(StrEnum):
    """Supported consultation languages."""

    ENGLISH = "English"
    HINDI = "Hindi"
    BENGALI = "Bengali"
    MARATHI = "Marathi"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    KANNADA = "Kannada"
    MALAYALAM = "Malayalam"
    ODIA = "Odia"


# ============================================================================
# Media
# ============================================================================

class MediaType(StrEnum):
    """Supported uploaded media."""

    IMAGE = "Image"
    AUDIO = "Audio"
    PDF = "PDF"


# ============================================================================
# Disease Knowledge
# ============================================================================

class DiseaseCategory(StrEnum):
    """Disease categories."""

    INFECTIOUS = "Infectious"
    RESPIRATORY = "Respiratory"
    CARDIOVASCULAR = "Cardiovascular"
    GASTROINTESTINAL = "Gastrointestinal"
    DERMATOLOGY = "Dermatology"
    NEUROLOGY = "Neurology"
    ENDOCRINE = "Endocrine"
    OTHER = "Other"


# ============================================================================
# UI
# ============================================================================

class Theme(StrEnum):
    """Application themes."""

    LIGHT = "Light"
    DARK = "Dark"
    SYSTEM = "System"


class Module(StrEnum):
    """Main application modules."""

    DASHBOARD = "Dashboard"
    PATIENTS = "Patients"
    CONSULTATIONS = "Consultations"
    AI = "AI"
    REPORTS = "Reports"
    KNOWLEDGE = "Knowledge Base"
    SETTINGS = "Settings"
    ADMIN = "Administration"