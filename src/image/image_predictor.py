"""
image_predictor.py

Loads the trained MobileNetV2 model and predicts
skin disease from an uploaded image.

Author : Sarwajit Kumar Mishra
Project : RuralCareAI
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import tensorflow as tf

from PIL import Image


class ImagePredictor:
    """
    MobileNetV2 Image Prediction Service
    """

    def __init__(self):

        project_root = Path(__file__).resolve().parents[2]

        self.model_path = (
            project_root
            / "models"
            / "mobilenet_skin.keras"
        )

        self.mapping_path = (
            project_root
            / "models"
            / "image_class_mapping.json"
        )

        self.image_size = (224, 224)

        self.model = self._load_model()

        self.class_mapping = self._load_mapping()

    # --------------------------------------------------

    def _load_model(self):

        if not self.model_path.exists():

            raise FileNotFoundError(
                f"Model not found : {self.model_path}"
            )

        return tf.keras.models.load_model(
            self.model_path
        )

    # --------------------------------------------------

    def _load_mapping(self):

        if not self.mapping_path.exists():

            raise FileNotFoundError(
                f"Class mapping not found : {self.mapping_path}"
            )

        with open(
            self.mapping_path,
            "r",
            encoding="utf-8",
        ) as fp:

            return json.load(fp)

    # --------------------------------------------------

    def _preprocess(self, image_path):

        image = Image.open(image_path)

        image = image.convert("RGB")

        image = image.resize(self.image_size)

        image = np.array(image)

        image = tf.keras.applications.mobilenet_v2.preprocess_input(
            image
        )

        image = np.expand_dims(
            image,
            axis=0,
        )

        return image

    # --------------------------------------------------

    def predict(self, image_path):

        image = self._preprocess(
            image_path
        )

        probabilities = self.model.predict(
            image,
            verbose=0,
        )[0]

        best_index = int(
            np.argmax(probabilities)
        )

        prediction = self.class_mapping[
            str(best_index)
        ]

        confidence = float(
            probabilities[best_index]
        )

        probability_table = {}

        for index, probability in enumerate(
            probabilities
        ):

            probability_table[
                self.class_mapping[str(index)]
            ] = round(
                float(probability),
                4,
            )

        return {

            "prediction": prediction,

            "confidence": confidence,

            "probabilities": probability_table,

        }


# ------------------------------------------------------


if __name__ == "__main__":

    predictor = ImagePredictor()

    result = predictor.predict(
        "sample.jpg"
    )

    print(result)