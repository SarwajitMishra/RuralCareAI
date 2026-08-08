"""
Fusion Engine

Combines:
1. Symptom-based Random Forest prediction
2. Skin Image prediction

Author:
Sarwajit Kumar Mishra
"""


class FusionEngine:

    SKIN_DISEASES = {
        "Fungal infection",
        "Psoriasis",
        "Impetigo",
        "Chicken pox"
    }

    def fuse(self, rf_result, image_result=None):

        # -----------------------------
        # No Image
        # -----------------------------
        if image_result is None:

            return {
                "final_prediction": rf_result["predicted_disease"],
                "confidence": rf_result["confidence"],
                "reason": "Prediction based on symptoms only."
            }

        rf_disease = rf_result["predicted_disease"]
        rf_conf = float(rf_result["confidence"])

        img_disease = image_result["prediction"]
        img_conf = float(image_result["confidence"]) * 100

        # -----------------------------
        # Same Prediction
        # -----------------------------
        if rf_disease.lower() == img_disease.lower():

            return {
                "final_prediction": rf_disease,
                "confidence": round((rf_conf + img_conf) / 2, 2),
                "reason": "Symptoms and image agree."
            }

        # -----------------------------
        # Skin Disease
        # -----------------------------
        if img_disease in self.SKIN_DISEASES:

            return {
                "final_prediction": img_disease,
                "confidence": round(img_conf, 2),
                "reason": "Image evidence is stronger for skin diseases."
            }

        # -----------------------------
        # Default
        # -----------------------------
        return {
            "final_prediction": rf_disease,
            "confidence": rf_conf,
            "reason": "Symptoms are more reliable for systemic diseases."
        }