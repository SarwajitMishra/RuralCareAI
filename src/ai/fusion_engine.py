"""
fusion_engine.py

Multimodal Fusion Engine

Combines predictions from multiple AI models
(Text, Image and future Voice) into one final
clinical decision.

Author : Sarwajit Kumar Mishra
Project : AI-Based Rural Healthcare Triage Assistant
"""

from __future__ import annotations


class FusionEngine:

    # Relative importance of each modality
    TEXT_WEIGHT = 0.70
    IMAGE_WEIGHT = 0.30

    def __init__(self):
        pass

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def fuse(
        self,
        text_prediction: dict,
        image_prediction: dict | None = None,
    ) -> dict:
        """
        Fuse text and image predictions.

        Parameters
        ----------
        text_prediction : dict
            Output from DiseasePredictor

        image_prediction : dict | None
            Output from ImagePredictor

        Returns
        -------
        dict
        """

        if image_prediction is None:
            return self._text_only(text_prediction)

        return self._text_image_fusion(
            text_prediction,
            image_prediction,
        )

    # --------------------------------------------------

    def _text_only(
        self,
        text: dict,
    ) -> dict:

        return {

            "fusion_prediction":
                text["predicted_disease"],

            "fusion_confidence":
                round(text["confidence"], 2),

            "agreement":
                False,

            "decision_source":
                "Text Model",

            "risk_level":
                text["risk_level"],

            "recommendation":
                text["recommendation"],

        }

    # --------------------------------------------------

    def _text_image_fusion(
        self,
        text: dict,
        image: dict,
    ) -> dict:

        text_disease = text["predicted_disease"]
        image_disease = image["prediction"]

        text_confidence = float(text["confidence"])

        image_confidence = float(image["confidence"])

        # Convert image confidence to percentage
        if image_confidence <= 1:
            image_confidence *= 100

        # ---------------------------------------------
        # Same disease
        # ---------------------------------------------

        if text_disease.lower() == image_disease.lower():

            confidence = (

                text_confidence * self.TEXT_WEIGHT +

                image_confidence * self.IMAGE_WEIGHT

            )

            return {

                "fusion_prediction":
                    text_disease,

                "fusion_confidence":
                    round(confidence, 2),

                "agreement":
                    True,

                "decision_source":
                    "Text + Image",

                "risk_level":
                    text["risk_level"],

                "recommendation":
                    text["recommendation"],

            }

        # ---------------------------------------------
        # Different diseases
        # ---------------------------------------------

        return {

            "fusion_prediction":
                text_disease,

            "fusion_confidence":
                round(text_confidence, 2),

            "agreement":
                False,

            "decision_source":
                "Text Model (Conflict)",

            "risk_level":
                text["risk_level"],

            "recommendation":
                text["recommendation"],

            "image_prediction":
                image_disease,

            "image_confidence":
                round(image_confidence, 2),

        }