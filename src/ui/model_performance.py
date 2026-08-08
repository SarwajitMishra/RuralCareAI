"""
Model Performance UI
"""

from pathlib import Path
import pickle

import pandas as pd
import streamlit as st
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
)

from src.ml.predictor import DiseasePredictor


@st.cache_resource
def load_model():

    predictor = DiseasePredictor()

    project_root = Path(__file__).resolve().parents[2]

    test_df = pd.read_csv(
        project_root / "data" / "Testing.csv"
    )

    test_df = test_df.loc[
        :,
        ~test_df.columns.str.contains("^Unnamed")
    ]

    X = test_df.drop(columns=["prognosis"])

    y = test_df["prognosis"]

    with open(
        project_root / "models" / "label_encoder.pkl",
        "rb",
    ) as file:

        encoder = pickle.load(file)

    y_true = encoder.transform(y)

    y_pred = predictor.model.predict(X)

    return predictor, encoder, y_true, y_pred


def show_model_performance():

    st.title("🤖 AI Model Performance")

    predictor, encoder, y_true, y_pred = load_model()

    accuracy = accuracy_score(
        y_true,
        y_pred,
    )

    st.metric(
        "Model Accuracy",
        f"{accuracy*100:.2f} %",
    )

    report = classification_report(
        y_true,
        y_pred,
        target_names=encoder.classes_,
        output_dict=True,
        zero_division=0,
    )

    report_df = pd.DataFrame(report).transpose()

    st.subheader("Classification Report")

    st.dataframe(
        report_df,
        use_container_width=True,
    )

    cm = confusion_matrix(
        y_true,
        y_pred,
    )

    st.subheader("Confusion Matrix")

    st.dataframe(
        pd.DataFrame(cm),
        use_container_width=True,
    )