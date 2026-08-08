"""
Disease Prediction Engine for RuralCareAI

This module loads the trained machine learning model and
provides disease prediction functionality.

Author: Sarwajit Kumar Mishra
"""

from pathlib import Path
import pickle

import numpy as np
import pandas as pd
import shap


class DiseasePredictor:
    """
    Disease prediction service using a trained Random Forest model.
    """

    def __init__(self):
        project_root = Path(__file__).resolve().parents[2]
        model_dir = project_root / "models"

        with open(model_dir / "random_forest.pkl", "rb") as f:
            self.model = pickle.load(f)

        with open(model_dir / "label_encoder.pkl", "rb") as f:
            self.label_encoder = pickle.load(f)

        with open(model_dir / "symptom_columns.pkl", "rb") as f:
            self.symptom_columns = pickle.load(f)

        self.explainer = shap.TreeExplainer(self.model)

    def _build_input_vector(self, selected_symptoms: list[str]) -> pd.DataFrame:
        """
        Convert a list of symptom names into the standardized
        binary feature vector expected by the model.
        """

        input_vector = np.zeros(len(self.symptom_columns))

        symptom_index = {
            symptom: idx
            for idx, symptom in enumerate(self.symptom_columns)
        }

        for symptom in selected_symptoms:
            if symptom in symptom_index:
                input_vector[symptom_index[symptom]] = 1

        return pd.DataFrame(
            [input_vector],
            columns=self.symptom_columns
        )

    def predict(self, selected_symptoms: list[str]) -> dict:
        """
        Predict disease from a list of selected symptoms.

        Example:
            predictor.predict([
                "itching",
                "skin_rash",
                "high_fever"
            ])
        """

        input_df = self._build_input_vector(selected_symptoms)

        # Predict disease
        prediction = self.model.predict(input_df)[0]

        disease = self.label_encoder.inverse_transform([prediction])[0]

        # Prediction probabilities
        probabilities = self.model.predict_proba(input_df)[0]

        top_indices = np.argsort(probabilities)[::-1][:3]

        top_predictions = []

        for idx in top_indices:
            top_predictions.append({
                "disease": self.label_encoder.inverse_transform([idx])[0],
                "confidence": round(float(probabilities[idx] * 100), 2)
            })

        confidence = round(float(max(probabilities) * 100), 2)

        if confidence >= 90:
            risk_level = "Critical"
        elif confidence >= 75:
            risk_level = "High"
        elif confidence >= 50:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            "predicted_disease": disease,
            "confidence": confidence,
            "risk_level": risk_level,
            "recommendation": self._get_recommendation(risk_level),
            "top_predictions": top_predictions
        }

    def get_all_symptoms(self):
        """
        Return all supported symptoms.
        """
        return sorted(self.symptom_columns)

    def explain_prediction(
            self,
            selected_symptoms,
    ):
        """
        Return the symptoms supplied by the user that contributed to
        the prediction, using real per-prediction SHAP values for the
        predicted class (positive = pushes toward the predicted
        disease, negative = pushes away from it).

        Falls back to the model's global feature importances if SHAP
        computation is unavailable for any reason.
        """

        input_df = self._build_input_vector(selected_symptoms)
        prediction = self.model.predict(input_df)[0]

        explanation = []

        try:
            shap_output = self.explainer(input_df)
            values = np.array(shap_output.values)

            class_index = list(self.model.classes_).index(prediction)

            if values.ndim == 3:
                # shape: (samples, features, classes)
                row = values[0, :, class_index]
            elif values.ndim == 2:
                # shape: (samples, features) - single-output explainer
                row = values[0]
            else:
                row = None

            if row is not None:
                shap_by_symptom = dict(zip(self.symptom_columns, row))

                for symptom in selected_symptoms:
                    if symptom in shap_by_symptom:
                        explanation.append({
                            "Symptom": symptom,
                            "Importance": float(shap_by_symptom[symptom]),
                        })

        except Exception:
            explanation = []

        if not explanation:
            # Fallback: global feature importance (not per-prediction)
            feature_importance = dict(
                zip(
                    self.symptom_columns,
                    self.model.feature_importances_,
                )
            )

            for symptom in selected_symptoms:
                explanation.append({
                    "Symptom": symptom,
                    "Importance": float(feature_importance.get(symptom, 0)),
                })

        explanation.sort(
            key=lambda x: abs(x["Importance"]),
            reverse=True,
        )

        return explanation

    def _get_recommendation(self, risk_level):

        recommendations = {

            "Critical": "Immediate emergency medical attention is recommended.",

            "High": "Consult a physician as soon as possible.",

            "Medium": "Clinical evaluation and follow-up are recommended.",

            "Low": "Home care, medication as advised, and monitor symptoms."

        }

        return recommendations[risk_level]