import os

import google.generativeai as genai


class GemmaService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            self.enabled = False
            return

        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel("gemma-3-12b-it")

        self.enabled = True

    def generate_summary(

            self,

            symptoms,

            prediction,

            confidence,

            image_prediction=None,

            medical_history=None,

    ):

        if not self.enabled:

            return (
                "LLM summary unavailable. "
                "Prediction generated using the AI models."
            )

        prompt = f"""
You are a rural healthcare assistant.

Patient Symptoms:
{", ".join(symptoms)}

Predicted Disease:
{prediction}

Prediction Confidence:
{confidence:.2f}%

Image Prediction:
{image_prediction}

Medical History:
{medical_history}

Generate:

1. Short clinical summary.
2. Possible reason.
3. Immediate advice.
4. When patient should visit hospital.

Maximum 150 words.
"""

        response = self.model.generate_content(prompt)

        return response.text