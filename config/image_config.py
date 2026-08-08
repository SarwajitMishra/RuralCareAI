"""
Image Module Configuration

Author: Sarwajit Kumar Mishra
Project: RuralCareAI
"""

from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_ROOT = PROJECT_ROOT / "datasets"

HAM10000_ROOT = DATASET_ROOT / "HAM10000"

IMAGE_FOLDER_1 = HAM10000_ROOT / "HAM10000_images_part_1"
IMAGE_FOLDER_2 = HAM10000_ROOT / "HAM10000_images_part_2"

METADATA_FILE = HAM10000_ROOT / "HAM10000_metadata.csv"

OUTPUT_DATASET = DATASET_ROOT / "skin"

# ==========================================================
# IMAGE SETTINGS
# ==========================================================

IMAGE_SIZE = (224, 224)

# Number of images per class
IMAGES_PER_CLASS = 100

# Dataset split
TRAIN_SPLIT = 0.70
VALIDATION_SPLIT = 0.15
TEST_SPLIT = 0.15

# Reproducibility
RANDOM_SEED = 42

# Supported HAM10000 classes

CLASS_MAPPING = {

    "akiec": "Actinic_Keratosis",

    "bcc": "Basal_Cell_Carcinoma",

    "bkl": "Benign_Keratosis",

    "df": "Dermatofibroma",

    "mel": "Melanoma",

    "nv": "Melanocytic_Nevus",

    "vasc": "Vascular_Lesion",

}