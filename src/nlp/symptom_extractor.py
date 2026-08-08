"""
============================================================
RuralCareAI
NLP Symptom Extractor

Pipeline

Text
 ↓
Normalize
 ↓
Medical Concept Detection
 ↓
Alias Matching
 ↓
Fuzzy Matching
 ↓
Validated Symptoms
============================================================
"""

import re

from .text_normalizer import TextNormalizer
from .symptom_dictionary import SymptomDictionary
from .fuzzy_matcher import FuzzyMatcher


class SymptomExtractor:

    def __init__(self):

        self.dictionary = SymptomDictionary()

        self.fuzzy = FuzzyMatcher(
            self.dictionary
        )

    # -----------------------------------------------------

    def extract(self, text):

        text = TextNormalizer.normalize(text)

        detected = set()

        matched_phrases = []

        unknown_words = []

        # -----------------------------------------------
        # Medical Concept Detection
        # -----------------------------------------------

        for concept, symptoms in self.dictionary.get_medical_concepts().items():

            if concept in text:

                matched_phrases.append(concept)

                detected.update(symptoms)

                text = text.replace(concept, " ")

        # -----------------------------------------------
        # Phrase Matching
        # -----------------------------------------------

        aliases = self.dictionary.get_all_aliases()

        for alias, symptom in aliases.items():

            if alias in text:

                detected.add(symptom)

                matched_phrases.append(alias)

                text = text.replace(alias, " ")

        # -----------------------------------------------
        # Token Matching
        # -----------------------------------------------

        words = re.findall(r"\b[a-zA-Z]+\b", text)

        for word in words:

            symptom = self.dictionary.lookup_alias(word)

            if symptom:

                detected.add(symptom)

                matched_phrases.append(word)

                continue

            symptom = self.fuzzy.match(word)

            if symptom:

                detected.add(symptom)

                matched_phrases.append(word)

            else:

                unknown_words.append(word)

        # -----------------------------------------------
        # Validation
        # -----------------------------------------------

        valid = []

        for symptom in detected:

            if self.dictionary.is_valid_symptom(symptom):

                valid.append(symptom)

        valid = sorted(list(set(valid)))

        # -----------------------------------------------
        # Confidence
        # -----------------------------------------------

        total = len(valid) + len(unknown_words)

        if total == 0:

            confidence = 0

        else:

            confidence = round(
                len(valid) / total,
                2
            )

        return {

            "detected_symptoms": valid,

            "matched_phrases": sorted(
                list(set(matched_phrases))
            ),

            "unknown_words": sorted(
                list(set(unknown_words))
            ),

            "confidence": confidence

        }