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
import re

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
        language: str = "English",
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
        language : str
            "English", "Hindi", or "Hinglish" - the language the
            summary itself should be written in, matching the input
            language options already offered for symptoms.
        """

        prompt = self._build_prompt(patient, symptoms, prediction, knowledge, language)

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

            report = data["response"].strip()
            report = self._isolate_final_report(report)
            report = self._renumber_sections(report)
            report = self._strip_meta_commentary(report)

            return report

        except requests.exceptions.ConnectionError:
            return (
                "AI clinical summary unavailable: could not reach the local "
                "Ollama server at localhost:11434. Make sure Ollama is "
                "running and the gemma3 model has been pulled."
            )

        except Exception as ex:
            return f"AI clinical summary unavailable: {ex}"

    # -----------------------------------------------------
    # Output cleanup
    # -----------------------------------------------------

    _SECTION_LABELS = (
        "Clinical Summary",
        "Possible Reasoning",
        "Immediate Advice",
        "Home Care",
        "Red Flag Symptoms",
        "Referral Recommendation",
    )

    @staticmethod
    def _label_regex(label: str) -> str:
        # Small models sometimes drop the space between words in a
        # heading (e.g. "ImmediateAdvice", "ReferralRecommendation");
        # matching word-by-word with an optional gap catches both.
        return r"\s*".join(re.escape(word) for word in label.split())

    @classmethod
    def _isolate_final_report(cls, text: str) -> str:
        """
        Small local models sometimes echo the six section headings
        twice: once as a bare outline with no content (or with a
        chatty "here's a draft" preamble tacked onto the last line),
        then again with the real content - continuing the numbering
        from where the outline left off (e.g. "7. Clinical Summary")
        instead of restarting at 1. If the first section's heading
        appears more than once, keep only from its LAST occurrence
        onward, discarding whatever duplicate preamble precedes it.
        """

        pattern = re.compile(
            r"^\s*\d+\.\s*\**\s*" + cls._label_regex(cls._SECTION_LABELS[0])
            + r"\s*\**:?\s*$",
            re.IGNORECASE | re.MULTILINE,
        )

        matches = list(pattern.finditer(text))

        if len(matches) > 1:
            text = text[matches[-1].start():]

        return text

    @classmethod
    def _renumber_sections(cls, text: str) -> str:
        """
        Force canonical "1. Clinical Summary" ... "6. Referral
        Recommendation" numbering on whichever six heading lines
        appear, in order, regardless of what numbers or spacing the
        model produced - a defensive backstop after _isolate_final_report
        may have left content starting at "7." instead of "1.".
        """

        lines = text.split("\n")
        next_label = 0

        for i, line in enumerate(lines):

            if next_label >= len(cls._SECTION_LABELS):
                break

            label = cls._SECTION_LABELS[next_label]

            heading_re = re.compile(
                r"^\s*\d+\.\s*\**\s*" + cls._label_regex(label) + r"\s*\**:?\s*$",
                re.IGNORECASE,
            )

            if heading_re.match(line.strip()):
                lines[i] = f"{next_label + 1}. {label}"
                next_label += 1

        return "\n".join(lines)

    _META_COMMENTARY_MARKERS = (
        "i've", "i have", "let me know", "please let me know",
        "hope this helps", "note:", "as requested", "i adhered",
        "i've adhered", "i have adhered", "feel free", "translation:",
        "(translation", "english translation",
    )

    @classmethod
    def _strip_meta_commentary(cls, text: str) -> str:
        """
        Small local models sometimes append a chatty sign-off after the
        requested sections (e.g. "Let me know if you'd like it tweaked!").
        Trim any trailing paragraph that reads as commentary about the
        instructions rather than clinical content - a defensive backstop
        for when the prompt's own "no meta-commentary" instruction isn't
        followed.
        """

        paragraphs = text.strip().split("\n\n")

        while paragraphs:
            last = paragraphs[-1].strip().lower()

            if any(last.startswith(marker) for marker in cls._META_COMMENTARY_MARKERS):
                paragraphs.pop()
            else:
                break

        return "\n\n".join(paragraphs).strip()

    # -----------------------------------------------------
    # Prompt construction
    # -----------------------------------------------------

    _LANGUAGE_INSTRUCTIONS = {
        "English": "Write the entire report in English.",
        "Hindi": (
            "CRITICAL LANGUAGE INSTRUCTION: Write your entire response in "
            "Hindi, using Devanagari script throughout (including the "
            "section headings). Do NOT use English, Spanish, French, or "
            "any other language - every word must be Hindi/Devanagari.\n"
            "Example of the required script: "
            "\"रोगी को बुखार और खांसी है। तुरंत डॉक्टर से मिलें।\""
        ),
        "Hinglish": (
            "CRITICAL LANGUAGE INSTRUCTION: Write your entire response in "
            "Hinglish - Hindi words and sentence structure spelled out "
            "phonetically using plain English/Roman letters (NOT "
            "Devanagari script, NOT pure English, NOT any other "
            "language) - the casual style used in everyday Indian text "
            "messages.\n"
            "Example: \"Patient ko tez bukhar aur khansi hai. Turant "
            "doctor se milna chahiye.\""
        ),
    }

    @staticmethod
    def _build_prompt(
        patient,
        symptoms: list[str],
        prediction: dict,
        knowledge: dict | None,
        language: str = "English",
    ) -> str:

        knowledge = knowledge or {}

        language_instruction = LLMService._LANGUAGE_INSTRUCTIONS.get(
            language, LLMService._LANGUAGE_INSTRUCTIONS["English"]
        )

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
{language_instruction}

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
Output ONLY the six numbered sections above, in a professional
clinical tone. Do not add any introduction, sign-off, meta-commentary
about these instructions, or offer to revise the report - the response
begins directly with "1. Clinical Summary" and ends after section 6.
Write each heading exactly ONCE, followed immediately by its content -
do not list the six headings as a bare outline before writing them
again with content, and do not restart or continue the numbering a
second time.

Reminder - {language_instruction}
"""
