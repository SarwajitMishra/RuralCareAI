"""
Multimodal Fusion Engine

Combines the symptom-based (Random Forest) prediction with the
optional skin-image (CNN) prediction using a late-fusion strategy,
so each modality can be optimized independently while still
contributing to a single final disease prediction.

Author: Sarwajit Kumar Mishra
"""

from __future__ import annotations


class FusionEngine:

    # Relative importance of each modality when they agree
    TEXT_WEIGHT = 0.70
    IMAGE_WEIGHT = 0.30

    # Dermatological classes for which visual evidence is treated as
    # more reliable than symptom text alone when the two disagree.
    SKIN_DISEASES = {
        "Fungal infection",
        "Psoriasis",
        "Impetigo",
        "Chicken pox",
        "Acne",
    }

    # Minimum image confidence (%) required to override the text
    # prediction on disagreement.
    IMAGE_OVERRIDE_THRESHOLD = 50.0

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def fuse(
        self,
        text_prediction: dict,
        image_prediction: dict | None = None,
    ) -> dict:
        """
        Fuse text and image predictions into a single result.

        Parameters
        ----------
        text_prediction : dict
            Output from DiseasePredictor / ConsultationService.predict().
        image_prediction : dict | None
            Output from ImagePredictor / ImageService.predict().

        Returns
        -------
        dict with keys: predicted_disease, confidence, agreement,
        decision_source, risk_level, recommendation, and (when an
        image was supplied) image_prediction, image_confidence.
        """

        if image_prediction is None:
            return self._text_only(text_prediction)

        return self._text_image_fusion(text_prediction, image_prediction)

    # --------------------------------------------------
    # Text only
    # --------------------------------------------------

    def _text_only(self, text: dict) -> dict:

        return {
            "predicted_disease": text["predicted_disease"],
            "confidence": round(float(text["confidence"]), 2),
            "agreement": False,
            "decision_source": "Text Model",
            "risk_level": text["risk_level"],
            "recommendation": text["recommendation"],
        }

    # --------------------------------------------------
    # Text + Image
    # --------------------------------------------------

    def _text_image_fusion(self, text: dict, image: dict) -> dict:

        text_disease = text["predicted_disease"]
        image_disease = image["prediction"]

        text_confidence = float(text["confidence"])
        image_confidence = float(image["confidence"])

        # Convert image confidence to percentage if it's a 0-1 fraction
        if image_confidence <= 1:
            image_confidence *= 100

        # ---------------------------------------------
        # Agreement: weighted score-level fusion
        # ---------------------------------------------

        if text_disease.lower() == image_disease.lower():

            confidence = (
                text_confidence * self.TEXT_WEIGHT
                + image_confidence * self.IMAGE_WEIGHT
            )

            return {
                "predicted_disease": text_disease,
                "confidence": round(confidence, 2),
                "agreement": True,
                "decision_source": "Text + Image (Agreement)",
                "risk_level": text["risk_level"],
                "recommendation": text["recommendation"],
                "image_prediction": image_disease,
                "image_confidence": round(image_confidence, 2),
            }

        # ---------------------------------------------
        # Disagreement: trust strong visual evidence for
        # known dermatological classes, otherwise trust symptoms
        # (systemic diseases are not visually diagnosable).
        # ---------------------------------------------

        if (
            image_disease in self.SKIN_DISEASES
            and image_confidence >= self.IMAGE_OVERRIDE_THRESHOLD
        ):
            return {
                "predicted_disease": image_disease,
                "confidence": round(image_confidence, 2),
                "agreement": False,
                "decision_source": "Image Model (Skin Disease Override)",
                "risk_level": text["risk_level"],
                "recommendation": text["recommendation"],
                "image_prediction": image_disease,
                "image_confidence": round(image_confidence, 2),
            }

        return {
            "predicted_disease": text_disease,
            "confidence": round(text_confidence, 2),
            "agreement": False,
            "decision_source": "Text Model (Conflict)",
            "risk_level": text["risk_level"],
            "recommendation": text["recommendation"],
            "image_prediction": image_disease,
            "image_confidence": round(image_confidence, 2),
        }
