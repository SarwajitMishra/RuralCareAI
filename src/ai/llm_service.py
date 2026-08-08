"""
Offline LLM Service using Ollama + Gemma 3
"""

from __future__ import annotations

import json
import requests


class LLMService:

    def __init__(self):

        self.url = "http://localhost:11434/api/generate"

        self.model = "gemma3:1b"

    # -----------------------------------------------------

    def generate_report(

        self,

        patient,

        symptoms,

        prediction,

    ) -> str:

        prompt = self._build_prompt(

            patient,

            symptoms,

            prediction,

        )

        return self._call_model(prompt)

    # -----------------------------------------------------

    def _call_model(self, prompt):

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False,

        }

        try:

            response = requests.post(

                self.url,

                json=payload,

                timeout=120,

            )

            response.raise_for_status()

            data = response.json()

            return data["response"]

        except Exception as ex:

            return f"LLM Error: {ex}"

    # -----------------------------------------------------

    def _build_prompt(

        self,

        patient,

        symptoms,

        prediction,

    ):

        return f"""
You are an experienced rural healthcare physician.

Patient

Name: {patient.full_name}

Age: {patient.age}

Gender: {patient.gender}

Symptoms

{", ".join(symptoms)}

AI Diagnosis

Disease:
{prediction["fusion_prediction"]}

Confidence:
{prediction["fusion_confidence"]:.2f}%

Risk:
{prediction["risk_level"]}

Recommendation:
{prediction["recommendation"]}

Generate a report using these headings only:

1. Clinical Summary

2. Possible Reasoning

3. Immediate Advice

4. Home Care

5. Red Flag Symptoms

6. Referral Recommendation

Do not prescribe medicines.

Mention that the AI is an assistant and not a replacement for a doctor.
"""