"""
Dataset Preparation Script

Creates a balanced dataset from HAM10000.

Author:
Sarwajit Kumar Mishra
"""

import random
import shutil
from pathlib import Path

import pandas as pd

from config.image_config import (
    CLASS_MAPPING,
    IMAGE_FOLDER_1,
    IMAGE_FOLDER_2,
    IMAGES_PER_CLASS,
    METADATA_FILE,
    OUTPUT_DATASET,
    RANDOM_SEED,
    TEST_SPLIT,
    TRAIN_SPLIT,
    VALIDATION_SPLIT,
)

random.seed(RANDOM_SEED)


class DatasetPreparation:

    def __init__(self):

        self.metadata = pd.read_csv(METADATA_FILE)

        self.image_lookup = {}

        self._build_image_lookup()

    def _build_image_lookup(self):

        print("Scanning image folders...")

        for folder in [IMAGE_FOLDER_1, IMAGE_FOLDER_2]:

            for image in folder.glob("*.jpg"):

                self.image_lookup[image.stem] = image

        print(f"Images found : {len(self.image_lookup)}")

    def prepare(self):

        if OUTPUT_DATASET.exists():

            shutil.rmtree(OUTPUT_DATASET)

        OUTPUT_DATASET.mkdir(parents=True)

        summary = []

        for class_code, class_name in CLASS_MAPPING.items():

            print(f"\nProcessing {class_name}")

            df = self.metadata[
                self.metadata["dx"] == class_code
            ]

            sample_size = min(
                IMAGES_PER_CLASS,
                len(df)
            )

            df = df.sample(
                sample_size,
                random_state=RANDOM_SEED
            )

            rows = df.to_dict("records")

            random.shuffle(rows)

            total = len(rows)

            train_end = int(total * TRAIN_SPLIT)

            val_end = train_end + int(
                total * VALIDATION_SPLIT
            )

            splits = {

                "train": rows[:train_end],

                "validation": rows[
                    train_end:val_end
                ],

                "test": rows[val_end:],

            }

            for split, records in splits.items():

                output_folder = (
                    OUTPUT_DATASET
                    / split
                    / class_name
                )

                output_folder.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                for record in records:

                    image_id = record["image_id"]

                    source = self.image_lookup.get(
                        image_id
                    )

                    if source is None:

                        continue

                    shutil.copy2(
                        source,
                        output_folder / source.name
                    )

                summary.append({

                    "Class": class_name,

                    "Split": split,

                    "Images": len(records),

                })

        summary_df = pd.DataFrame(summary)

        summary_df.to_csv(

            OUTPUT_DATASET / "dataset_summary.csv",

            index=False,

        )

        print("\nDataset Created Successfully\n")

        print(summary_df)


if __name__ == "__main__":

    DatasetPreparation().prepare()