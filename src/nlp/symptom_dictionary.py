"""
============================================================
RuralCareAI
Medical Knowledge Base

This module is responsible for:
1. Loading official Random Forest symptoms
2. Automatic alias generation
3. English/Hindi/Hinglish synonym mapping
4. Medical concept expansion (Part 2)
============================================================
"""

from pathlib import Path
import pickle


class SymptomDictionary:

    def __init__(self):

        self.standard_symptoms = self._load_standard_symptoms()

        self.alias_map = self._generate_default_aliases()

        self._load_manual_aliases()

        self._load_medical_concepts()

    # -----------------------------------------------------
    # Load Random Forest symptom names
    # -----------------------------------------------------

    def _load_standard_symptoms(self):

        model_path = (
            Path(__file__).resolve().parents[2]
            / "models"
            / "symptom_columns.pkl"
        )

        with open(model_path, "rb") as f:
            symptoms = pickle.load(f)

        return symptoms

    # -----------------------------------------------------
    # Automatically generate aliases
    # Example:
    #
    # high_fever
    #
    # becomes
    #
    # high fever
    # High Fever
    # high_fever
    # -----------------------------------------------------

    def _generate_default_aliases(self):

        aliases = {}

        for symptom in self.standard_symptoms:

            generated = set()

            generated.add(symptom)

            generated.add(
                symptom.replace("_", " ")
            )

            generated.add(
                symptom.replace("_", " ").lower()
            )

            generated.add(
                symptom.replace("_", " ").title()
            )

            aliases[symptom] = generated

        return aliases

    # -----------------------------------------------------
    # Human knowledge
    # -----------------------------------------------------

    def _load_manual_aliases(self):

        self._add(
            "high_fever",
            [
                "fever",
                "high fever",
                "continuous fever",
                "persistent fever",
                "repeated fever",
                "temperature",
                "body temperature",
                "bukhar",
                "tez bukhar",
                "bahut bukhar"
            ]
        )

        self._add(
            "mild_fever",
            [
                "mild fever",
                "slight fever",
                "low fever",
                "light fever",
                "kam bukhar"
            ]
        )

        self._add(
            "cough",
            [
                "cough",
                "dry cough",
                "wet cough",
                "khansi",
                "khaasi",
                "lagatar khansi"
            ]
        )

        self._add(
            "continuous_sneezing",
            [
                "continuous sneezing",
                "constant sneezing",
                "sneezing continuously",
                "baar baar chheenk",
                "chheenk"
            ]
        )

        self._add(
            "vomiting",
            [
                "vomiting",
                "vomit",
                "throwing up",
                "puking",
                "ulti",
                "ulti ho rahi hai"
            ]
        )

        self._add(
            "nausea",
            [
                "nausea",
                "feeling sick",
                "vomit feeling",
                "jee machalna"
            ]
        )

        self._add(
            "diarrhoea",
            [
                "diarrhea",
                "diarrhoea",
                "loose motion",
                "loose motions",
                "motion problem",
                "dast",
                "baar baar motion"
            ]
        )

        self._add(
            "stomach_pain",
            [
                "stomach pain",
                "stomach ache",
                "pet dard",
                "pet me dard",
                "pet dukh raha hai"
            ]
        )

        self._add(
            "abdominal_pain",
            [
                "abdominal pain",
                "abdomen pain",
                "pain in abdomen"
            ]
        )

        self._add(
            "belly_pain",
            [
                "belly pain",
                "pain in belly"
            ]
        )

        self._add(
            "headache",
            [
                "headache",
                "head ache",
                "sir dard",
                "sar dard"
            ]
        )

        self._add(
            "chest_pain",
            [
                "chest pain",
                "pain in chest",
                "seene me dard"
            ]
        )

        self._add(
            "breathlessness",
            [
                "shortness of breath",
                "breathing difficulty",
                "difficulty breathing",
                "saans lene me dikkat",
                "saans phoolna"
            ]
        )

        self._add(
            "fatigue",
            [
                "fatigue",
                "tired",
                "weakness",
                "thakan",
                "kamjori"
            ]
        )

        self._add(
            "joint_pain",
            [
                "joint pain",
                "pain in joints",
                "ghutne dard",
                "joint ache"
            ]
        )

        self._add(
            "muscle_pain",
            [
                "muscle pain",
                "body pain",
                "body ache",
                "sharir dard"
            ]
        )

        self._add(
            "back_pain",
            [
                "back pain",
                "lower back pain",
                "peeth dard"
            ]
        )

        self._add(
            "burning_micturition",
            [
                "burning urine",
                "burning urination",
                "pain while urinating",
                "jalan peshab"
            ]
        )

        self._add(
            "skin_rash",
            [
                "skin rash",
                "rashes",
                "red rash",
                "chakate"
            ]
        )

        self._add(
            "itching",
            [
                "itching",
                "itch",
                "khujli"
            ]
        )

    # -----------------------------------------------------
    # Utility
    # -----------------------------------------------------

    def _add(self, symptom, words):

        if symptom not in self.alias_map:
            return

        self.alias_map[symptom].update(
            [w.lower() for w in words]
        )

    # -----------------------------------------------------
    # Medical Concepts
    # These are NOT symptoms.
    # They expand into one or more standardized symptoms.
    # -----------------------------------------------------

    def _load_medical_concepts(self):

        self.medical_concepts = {

            "food poisoning": [
                "vomiting",
                "nausea",
                "diarrhoea",
                "stomach_pain",
                "abdominal_pain",
                "dehydration"
            ],

            "stomach infection": [
                "stomach_pain",
                "abdominal_pain",
                "diarrhoea",
                "vomiting"
            ],

            "viral fever": [
                "high_fever",
                "fatigue",
                "headache",
                "body_pain"
            ],

            "common cold": [
                "continuous_sneezing",
                "runny_nose",
                "congestion",
                "mild_fever",
                "cough"
            ],

            "flu": [
                "high_fever",
                "cough",
                "fatigue",
                "body_pain",
                "headache"
            ],

            "gas problem": [
                "acidity",
                "indigestion",
                "stomach_pain",
                "abdominal_pain"
            ],

            "urine infection": [
                "burning_micturition",
                "bladder_discomfort",
                "continuous_feel_of_urine"
            ],

            "uti": [
                "burning_micturition",
                "bladder_discomfort",
                "continuous_feel_of_urine"
            ],

            "allergy": [
                "continuous_sneezing",
                "itching",
                "skin_rash"
            ]
        }

    # -----------------------------------------------------
    # Reverse Lookup
    # -----------------------------------------------------

    def get_all_aliases(self):

        aliases = {}

        for symptom, words in self.alias_map.items():

            for word in words:

                aliases[word.lower()] = symptom

        return aliases


    # -----------------------------------------------------

    def get_standard_symptoms(self):

        return self.standard_symptoms


    # -----------------------------------------------------

    def get_medical_concepts(self):

        return self.medical_concepts


    # -----------------------------------------------------

    def is_valid_symptom(self, symptom):

        return symptom in self.standard_symptoms


    # -----------------------------------------------------

    def expand_medical_concept(self, phrase):

        phrase = phrase.lower().strip()

        return self.medical_concepts.get(phrase, [])


    # -----------------------------------------------------

    def lookup_alias(self, phrase):

        phrase = phrase.lower().strip()

        for symptom, aliases in self.alias_map.items():

            if phrase in aliases:

                return symptom

        return None