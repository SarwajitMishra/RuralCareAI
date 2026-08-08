"""
image_service.py

Service layer for image classification.

Responsibilities:
- Validate uploaded image
- Save uploaded image
- Cache the MobileNetV2 model
- Return prediction result

Author: Sarwajit Kumar Mishra
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import BinaryIO

from PIL import Image

from src.image.image_predictor import ImagePredictor


class ImageService:
    """
    Service responsible for image validation,
    storage and prediction.
    """

    _predictor = None

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.upload_folder = (
            self.project_root
            / "uploads"
            / "images"
        )

        self.upload_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        if ImageService._predictor is None:
            ImageService._predictor = ImagePredictor()

    # ----------------------------------------------------

    def validate_image(self, uploaded_file) -> bool:
        """
        Verify that the uploaded file is a valid image.
        """

        try:

            image = Image.open(uploaded_file)

            image.verify()

            uploaded_file.seek(0)

            return True

        except Exception:

            return False

    # ----------------------------------------------------

    def save_image(self, uploaded_file) -> Path:
        """
        Save uploaded image with unique filename.
        """

        extension = Path(uploaded_file.name).suffix.lower()

        filename = (
            f"{uuid.uuid4().hex}{extension}"
        )

        destination = (
            self.upload_folder
            / filename
        )

        with open(destination, "wb") as file:

            file.write(uploaded_file.getbuffer())

        return destination

    # ----------------------------------------------------

    def predict(self, uploaded_file):
        """
        Complete workflow:
            Validate
            Save
            Predict
        """

        if not self.validate_image(uploaded_file):

            raise ValueError(
                "Uploaded file is not a valid image."
            )

        saved_image = self.save_image(
            uploaded_file
        )

        prediction = (
            ImageService._predictor.predict(
                saved_image
            )
        )

        prediction["image_path"] = str(
            saved_image
        )

        return prediction