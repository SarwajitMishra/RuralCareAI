"""
Local LLM Module for RuralCareAI.

Generates an AI-assisted clinical summary using Gemma 3, executed
locally through Ollama. The prompt is grounded with the disease
knowledge retrieved by the Knowledge Retrieval Module (RAG), so the
generated recommendations stay tied to verified healthcare content
rather than being freely generated.

Running the model locally keeps the application usable in
environments with limited or intermittent internet connectivity.

Author: Sarwajit Kumar Mishra
"""

from __future__ import annotations

import os

import requests


class LLMService:

    def __init__(self, model: str = "gemma3:1b"):
        # OLLAMA_HOST lets this point at a separate container (e.g. the
        # "ollama" service in docker-compose) instead of localhost.
        host = os.environ.get("OLLAMA_HOST", "localhost:11434")
        self.url = f"http://{host}/api/generate"
        self.model = model

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def generate_report(
        self,
        patient,
        symptoms: list[str],
        prediction: dict,
        knowledge: dict | None = None,
    ) -> str:
        """
        Generate an AI-assisted clinical summary.

        Parameters
        ----------
        patient : Patient
            The patient database record.
        symptoms : list[str]
            Machine-readable symptom names selected for this consultation.
        prediction : dict
            Final prediction dict, expected to contain at least
            'predicted_disease', 'confidence', 'risk_level',
            'recommendation'.
        knowledge : dict | None
            Retrieved knowledge-base entry for the predicted disease
            (description, precautions, first_aid, when_to_consult,
            emergency_signs) used to ground the summary.
        """

        prompt = self._build_prompt(patient, symptoms, prediction, knowledge)

        return self._call_model(prompt)

    # -----------------------------------------------------
    # Ollama call
    # -----------------------------------------------------

    def _call_model(self, prompt: str) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()

            data = response.json()

            return data["response"].strip()

        except requests.exceptions.ConnectionError:
            return (
                "AI clinical summary unavailable: could not reach the local "
                "Ollama server at localhost:11434. Make sure Ollama is "
                "running and the gemma3 model has been pulled."
            )

        except Exception as ex:
            return f"AI clinical summary unavailable: {ex}"

    # -----------------------------------------------------
    # Prompt construction
    # -----------------------------------------------------

    @staticmethod
    def _build_prompt(
        patient,
        symptoms: list[str],
        prediction: dict,
        knowledge: dict | None,
    ) -> str:

        knowledge = knowledge or {}

        readable_symptoms = ", ".join(
            symptom.replace("_", " ") for symptom in symptoms
        )

        precautions = "; ".join(knowledge.get("precautions", [])) or "Not available"
        first_aid = "; ".join(knowledge.get("first_aid", [])) or "Not available"
        emergency_signs = (
            "; ".join(knowledge.get("emergency_signs", [])) or "Not available"
        )
        when_to_consult = knowledge.get("when_to_consult", "Not available")

        return f"""
You are an experienced rural healthcare physician assisting a frontline
healthcare worker. Use ONLY the reference information provided below;
do not invent clinical facts beyond it.

Patient
Name: {patient.full_name}
Age: {patient.age}
Gender: {patient.gender}

Reported Symptoms
{readable_symptoms}

AI Prediction
Disease: {prediction.get("predicted_disease")}
Confidence: {prediction.get("confidence", 0):.2f}%
Risk Level: {prediction.get("risk_level")}
Recommendation: {prediction.get("recommendation")}

Reference Knowledge (verified)
Description: {knowledge.get("description", "Not available")}
Precautions: {precautions}
First Aid: {first_aid}
When to consult a doctor: {when_to_consult}
Emergency warning signs: {emergency_signs}

Generate a report using exactly these headings:

1. Clinical Summary
2. Possible Reasoning
3. Immediate Advice
4. Home Care
5. Red Flag Symptoms
6. Referral Recommendation

Keep the response under 200 words in total.
Do not prescribe medicines.
Mention that this is an AI-generated assistive summary and not a
replacement for a qualified doctor.
"""
