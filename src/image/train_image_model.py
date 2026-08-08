"""
train_image_model.py

Train a MobileNetV2 image classification model for RuralCareAI.

Author : Sarwajit Kumar Mishra
Project: AI-Based Rural Healthcare Triage Assistant using Multimodal
         Machine Learning

TensorFlow : 2.20+
"""

from __future__ import annotations

import json
from pathlib import Path

import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import callbacks
from tensorflow.keras import applications

# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = PROJECT_ROOT / "datasets" / "skin"

MODEL_PATH = PROJECT_ROOT / "models" / "mobilenet_skin.keras"

CLASS_MAPPING_PATH = (
    PROJECT_ROOT
    / "models"
    / "image_class_mapping.json"
)

METRICS_PATH = (
    PROJECT_ROOT
    / "models"
    / "image_training_metrics.json"
)

IMAGE_SIZE = (224, 224)

BATCH_SIZE = 16

EPOCHS = 15

SEED = 42

AUTOTUNE = tf.data.AUTOTUNE

# ============================================================
# Dataset Loader
# ============================================================


def load_dataset():

    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH / "train",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=SEED,
    )

    validation_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH / "validation",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    test_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_PATH / "test",
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    class_names = train_ds.class_names

    train_ds = train_ds.prefetch(AUTOTUNE)

    validation_ds = validation_ds.prefetch(AUTOTUNE)

    test_ds = test_ds.prefetch(AUTOTUNE)

    return (
        train_ds,
        validation_ds,
        test_ds,
        class_names,
    )


# ============================================================
# Data Augmentation
# ============================================================


def create_data_augmentation():

    return tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.05),
            layers.RandomZoom(0.10),
            layers.RandomContrast(0.10),
        ],
        name="augmentation",
    )


# ============================================================
# Model Builder
# ============================================================


def create_model(num_classes: int):

    data_augmentation = create_data_augmentation()

    preprocess = (
        applications.mobilenet_v2.preprocess_input
    )

    base_model = applications.MobileNetV2(

        input_shape=(224, 224, 3),

        include_top=False,

        weights="imagenet",

    )

    base_model.trainable = False

    inputs = layers.Input(
        shape=(224, 224, 3)
    )

    x = data_augmentation(inputs)

    x = preprocess(x)

    x = base_model(
        x,
        training=False,
    )

    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dropout(0.30)(x)

    x = layers.Dense(
        128,
        activation="relu",
    )(x)

    outputs = layers.Dense(
        num_classes,
        activation="softmax",
    )(x)

    model = models.Model(
        inputs,
        outputs,
    )

    model.compile(

        optimizer="adam",

        loss="sparse_categorical_crossentropy",

        metrics=[
            "accuracy",
        ],

    )

    return model

# ============================================================
# Callbacks
# ============================================================


def get_callbacks():

    checkpoint = callbacks.ModelCheckpoint(
        filepath=MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1,
    )

    early_stop = callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1,
    )

    reduce_lr = callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=1e-6,
        verbose=1,
    )

    return [
        checkpoint,
        early_stop,
        reduce_lr,
    ]


# ============================================================
# Metrics
# ============================================================


def save_class_mapping(class_names):

    mapping = {
        str(index): name
        for index, name in enumerate(class_names)
    }

    with open(
        CLASS_MAPPING_PATH,
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            mapping,
            fp,
            indent=4,
        )


def save_metrics(history, test_loss, test_accuracy):

    metrics = {

        "epochs": len(
            history.history["loss"]
        ),

        "train_accuracy": float(
            history.history["accuracy"][-1]
        ),

        "validation_accuracy": float(
            history.history["val_accuracy"][-1]
        ),

        "train_loss": float(
            history.history["loss"][-1]
        ),

        "validation_loss": float(
            history.history["val_loss"][-1]
        ),

        "test_accuracy": float(
            test_accuracy
        ),

        "test_loss": float(
            test_loss
        ),
    }

    with open(
        METRICS_PATH,
        "w",
        encoding="utf-8",
    ) as fp:

        json.dump(
            metrics,
            fp,
            indent=4,
        )


# ============================================================
# Training
# ============================================================


def train():

    (
        train_ds,
        validation_ds,
        test_ds,
        class_names,
    ) = load_dataset()

    print("\nClasses\n")

    for cls in class_names:
        print(cls)

    print()

    model = create_model(
        len(class_names)
    )

    model.summary()

    history = model.fit(

        train_ds,

        validation_data=validation_ds,

        epochs=EPOCHS,

        callbacks=get_callbacks(),

    )

    print("\nEvaluating model...\n")

    test_loss, test_accuracy = model.evaluate(
        test_ds,
        verbose=1,
    )

    save_class_mapping(
        class_names
    )

    save_metrics(
        history,
        test_loss,
        test_accuracy,
    )

    print("\nTraining Complete\n")

    print(
        f"Test Accuracy : {test_accuracy:.4f}"
    )

    print(
        f"Test Loss     : {test_loss:.4f}"
    )

    print(
        f"\nModel Saved : {MODEL_PATH}"
    )


# ============================================================
# Main
# ============================================================


if __name__ == "__main__":

    train()