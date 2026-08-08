"""
Healthcare Risk Assessment Engine for RuralCareAI.

Categorizes a patient into Low / Medium / High / Critical risk based
on the predicted disease's baseline severity, the model's prediction
confidence, existing chronic medical history, and the presence of
red-flag symptoms - assisting healthcare workers with preliminary
triage prioritization.

Author: Sarwajit Kumar Mishra
"""

from __future__ import annotations

from src.knowledge.data import get_disease_knowledge

# Symptoms that, on their own, indicate a potentially serious or
# emergency condition regardless of the predicted disease.
RED_FLAG_SYMPTOMS = {
    "chest_pain",
    "breathlessness",
    "coma",
    "altered_sensorium",
    "slurred_speech",
    "weakness_of_one_body_side",
    "stomach_bleeding",
    "blood_in_sputum",
    "fast_heart_rate",
}

# Chronic conditions (from the consultation UI's medical-history
# selector) that meaningfully elevate real-world clinical risk.
COMORBIDITY_BUMP = 15

RED_FLAG_BUMP = 15

RECOMMENDATIONS = {
    "Critical": "Immediate referral to the nearest emergency hospital.",
    "High": "Refer to a physician or district hospital within 24 hours.",
    "Medium": "Clinical evaluation and follow-up recommended.",
    "Low": "Home care, medication as advised, and monitor symptoms.",
}


class RiskEngine:
    """
    Unified risk assessment used across the consultation workflow.
    """

    @staticmethod
    def assess(
        disease: str,
        confidence: float,
        medical_history: list[str] | None = None,
        symptoms: list[str] | None = None,
    ) -> dict:
        """
        Compute a risk level for the given prediction.

        Returns
        -------
        dict with keys: level, score, recommendation, reasons
        """

        medical_history = medical_history or []
        symptoms = symptoms or []

        base_risk = get_disease_knowledge(disease).get("risk", 50)

        score = (0.7 * base_risk) + (0.3 * float(confidence))
        reasons = [
            f"Baseline severity for {disease}: {base_risk}/100",
            f"Prediction confidence: {confidence:.2f}%",
        ]

        if medical_history:
            score += COMORBIDITY_BUMP
            reasons.append(
                "Elevated due to existing chronic condition(s): "
                + ", ".join(medical_history)
            )

        matched_red_flags = RED_FLAG_SYMPTOMS.intersection(symptoms)

        if matched_red_flags:
            score += RED_FLAG_BUMP
            reasons.append(
                "Elevated due to red-flag symptom(s): "
                + ", ".join(sorted(matched_red_flags))
            )

        score = min(round(score, 2), 100.0)

        if score >= 85:
            level = "Critical"
        elif score >= 65:
            level = "High"
        elif score >= 40:
            level = "Medium"
        else:
            level = "Low"

        return {
            "level": level,
            "score": score,
            "recommendation": RECOMMENDATIONS[level],
            "reasons": reasons,
        }
