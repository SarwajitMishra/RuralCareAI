"""
Model Training Script for RuralCareAI

This script:
1. Loads the training and testing datasets.
2. Trains a Random Forest classifier.
3. Evaluates model accuracy.
4. Saves the trained model and supporting artifacts.

Author: Sarwajit Kumar Mishra
"""

from pathlib import Path
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder


# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"

TRAIN_FILE = DATA_DIR / "Training.csv"
TEST_FILE = DATA_DIR / "Testing.csv"

MODEL_DIR.mkdir(exist_ok=True)


# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

print("=" * 60)
print("RuralCareAI Model Training")
print("=" * 60)

print("\nLoading datasets...")

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

# Remove accidental index columns
train_df = train_df.loc[:, ~train_df.columns.str.contains("^Unnamed")]
test_df = test_df.loc[:, ~test_df.columns.str.contains("^Unnamed")]

print(f"Training Samples : {len(train_df)}")
print(f"Testing Samples  : {len(test_df)}")


# ----------------------------------------------------------
# Split Features and Labels
# ----------------------------------------------------------

X_train = train_df.drop(columns=["prognosis"])
y_train = train_df["prognosis"]

X_test = test_df.drop(columns=["prognosis"])
y_test = test_df["prognosis"]

print(f"Features         : {X_train.shape[1]}")
print(f"Diseases         : {y_train.nunique()}")


# ----------------------------------------------------------
# Encode Labels
# ----------------------------------------------------------

label_encoder = LabelEncoder()

y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)


# ----------------------------------------------------------
# Train Model
# ----------------------------------------------------------

print("\nTraining Random Forest Model...")

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train_encoded)

print("Training completed.")


# ----------------------------------------------------------
# Evaluate
# ----------------------------------------------------------

print("\nEvaluating model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test_encoded, predictions)

print(f"\nAccuracy : {accuracy * 100:.2f}%")

print("\nClassification Report\n")
print(
    classification_report(
        y_test_encoded,
        predictions,
        target_names=label_encoder.classes_,
        zero_division=0,
    )
)


# ----------------------------------------------------------
# Save Artifacts
# ----------------------------------------------------------

print("\nSaving model artifacts...")

with open(MODEL_DIR / "random_forest.pkl", "wb") as file:
    pickle.dump(model, file)

with open(MODEL_DIR / "label_encoder.pkl", "wb") as file:
    pickle.dump(label_encoder, file)

with open(MODEL_DIR / "symptom_columns.pkl", "wb") as file:
    pickle.dump(list(X_train.columns), file)

print("✓ random_forest.pkl")
print("✓ label_encoder.pkl")
print("✓ symptom_columns.pkl")

print("\nModel training completed successfully.")