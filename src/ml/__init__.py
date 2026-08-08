def explain_prediction(self, symptoms: list[str]) -> list[dict]:
    """
    Explain prediction using SHAP values.

    Returns
    -------
    [
        {
            "Symptom": "...",
            "Importance": ...
        }
    ]
    """

    # Build input vector
    input_vector = np.zeros(len(self.symptom_columns))

    for symptom in symptoms:

        if symptom in self.symptom_columns:

            index = self.symptom_columns.index(symptom)

            input_vector[index] = 1

    X = pd.DataFrame(
        [input_vector],
        columns=self.symptom_columns,
    )

    shap_values = self.explainer.shap_values(X)

    prediction = self.model.predict(X)[0]

    class_index = list(self.model.classes_).index(prediction)

    if isinstance(shap_values, list):
        values = shap_values[class_index][0]
    else:
        values = shap_values[0]

    explanation = []

    for feature, value in zip(
        self.symptom_columns,
        values,
    ):

        if abs(value) > 0:

            explanation.append(
                {
                    "Symptom": feature,
                    "Importance": abs(float(value)),
                }
            )

    explanation.sort(
        key=lambda x: x["Importance"],
        reverse=True,
    )

    return explanation[:10]