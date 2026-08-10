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
                "bahut bukhar",
                "बुखार",
                "तेज़ बुखार",
                "तेज बुखार",
            ]
        )

        self._add(
            "mild_fever",
            [
                "mild fever",
                "slight fever",
                "low fever",
                "light fever",
                "kam bukhar",
                "हल्का बुखार",
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
                "lagatar khansi",
                "खांसी",
                "खाँसी",
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
                "ulti ho rahi hai",
                "उल्टी",
                "वमन",
            ]
        )

        self._add(
            "nausea",
            [
                "nausea",
                "feeling sick",
                "vomit feeling",
                "jee machalna",
                "जी मिचलाना",
                "मतली",
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
                "baar baar motion",
                "दस्त",
                "पतले दस्त",
            ]
        )

        self._add(
            "stomach_pain",
            [
                "stomach pain",
                "stomach ache",
                "pet dard",
                "pet me dard",
                "pet dukh raha hai",
                "पेट दर्द",
                "पेट में दर्द",
            ]
        )

        self._add(
            "abdominal_pain",
            [
                "abdominal pain",
                "abdomen pain",
                "pain in abdomen",
                "pet ka dard",
                "पेट का दर्द",
            ]
        )

        self._add(
            "belly_pain",
            [
                "belly pain",
                "pain in belly",
                "pet mein marod",
                "marod utha",
                "पेट में मरोड़",
            ]
        )

        self._add(
            "headache",
            [
                "headache",
                "head ache",
                "sir dard",
                "sar dard",
                "सिर दर्द",
                "सर दर्द",
            ]
        )

        self._add(
            "chest_pain",
            [
                "chest pain",
                "pain in chest",
                "seene me dard",
                "seene mein dard",
                "सीने में दर्द",
                "छाती में दर्द",
            ]
        )

        self._add(
            "breathlessness",
            [
                "shortness of breath",
                "breathing difficulty",
                "difficulty breathing",
                "saans lene me dikkat",
                "saans phoolna",
                "सांस लेने में तकलीफ",
                "सांस फूलना",
            ]
        )

        self._add(
            "fatigue",
            [
                "fatigue",
                "tired",
                "weakness",
                "thakan",
                "kamjori",
                "कमजोरी",
                "थकान",
            ]
        )

        self._add(
            "joint_pain",
            [
                "joint pain",
                "pain in joints",
                "ghutne dard",
                "joint ache",
                "जोड़ों में दर्द",
            ]
        )

        self._add(
            "muscle_pain",
            [
                "muscle pain",
                "body pain",
                "body ache",
                "sharir dard",
                "बदन दर्द",
                "शरीर दर्द",
            ]
        )

        self._add(
            "back_pain",
            [
                "back pain",
                "lower back pain",
                "peeth dard",
                "पीठ दर्द",
            ]
        )

        self._add(
            "burning_micturition",
            [
                "burning urine",
                "burning urination",
                "pain while urinating",
                "jalan peshab",
                "पेशाब में जलन",
            ]
        )

        self._add(
            "skin_rash",
            [
                "skin rash",
                "rashes",
                "red rash",
                "chakate",
                "त्वचा पर दाने",
                "चकत्ते",
            ]
        )

        self._add(
            "itching",
            [
                "itching",
                "itch",
                "khujli",
                "खुजली",
            ]
        )

        # -----------------------------------------------------
        # Additional symptoms needed for common rural-disease demo
        # scenarios (Typhoid, Tuberculosis, Malaria, Jaundice, UTI) -
        # English, Hinglish, and Hindi (Devanagari) coverage.
        # -----------------------------------------------------

        self._add(
            "chills",
            [
                "chills",
                "shivering",
                "thand lagna",
                "kaanpna",
                "ठंड लगना",
                "कंपकंपी",
            ]
        )

        self._add(
            "sweating",
            [
                "sweating",
                "excessive sweating",
                "pasina",
                "pasina aana",
                "पसीना",
                "पसीना आना",
            ]
        )

        self._add(
            "dehydration",
            [
                "dehydration",
                "dehydrated",
                "paani ki kami",
                "पानी की कमी",
                "निर्जलीकरण",
            ]
        )

        self._add(
            "constipation",
            [
                "constipation",
                "kabj",
                "kabz",
                "कब्ज",
            ]
        )

        self._add(
            "weight_loss",
            [
                "weight loss",
                "losing weight",
                "wazan kam hona",
                "wazan ghatna",
                "वजन कम होना",
                "वजन घटना",
            ]
        )

        self._add(
            "loss_of_appetite",
            [
                "loss of appetite",
                "no appetite",
                "not feeling hungry",
                "bhookh na lagna",
                "bhookh kam hona",
                "भूख न लगना",
                "भूख कम होना",
            ]
        )

        self._add(
            "blood_in_sputum",
            [
                "blood in sputum",
                "blood in phlegm",
                "coughing blood",
                "cough with blood",
                "khoon wali khansi",
                "khansi me khoon",
                "balgam me khoon",
                "खांसी में खून",
                "बलगम में खून",
            ]
        )

        self._add(
            "nodal_skin_eruptions",
            [
                "skin eruptions",
                "nodal eruptions",
                "twacha par ubhar",
                "त्वचा पर गांठ",
                "त्वचा में उभार",
            ]
        )

        self._add(
            "dischromic _patches",
            [
                "discoloured patches",
                "discolored patches",
                "patches on skin",
                "rang badalna",
                "रंगीन धब्बे",
                "त्वचा का रंग बदलना",
            ]
        )

        self._add(
            "yellowish_skin",
            [
                "yellow skin",
                "yellowish skin",
                "peeli twacha",
                "त्वचा पीली होना",
                "पीली त्वचा",
            ]
        )

        self._add(
            "dark_urine",
            [
                "dark urine",
                "urine dark",
                "gehra peshab",
                "पेशाब का रंग गहरा",
                "गहरे रंग का पेशाब",
            ]
        )

        self._add(
            "bladder_discomfort",
            [
                "bladder discomfort",
                "bladder pain",
                "मूत्राशय में परेशानी",
            ]
        )

        self._add(
            "foul_smell_of urine",
            [
                "foul smell of urine",
                "smelly urine",
                "peshab me badbu",
                "पेशाब से बदबू",
            ]
        )

        self._add(
            "swelled_lymph_nodes",
            [
                "swollen lymph nodes",
                "swelled glands",
                "gaanth sujna",
                "granthi sujna",
                "गांठें सूजना",
                "गर्दन में सूजन",
            ]
        )

        self._add(
            "malaise",
            [
                "malaise",
                "general weakness",
                "sustee",
                "susti",
                "बेचैनी",
                "अस्वस्थता",
            ]
        )

        self._add(
            "phlegm",
            [
                "phlegm",
                "mucus",
                "kaff",
                "कफ",
            ]
        )

        self._add(
            "yellowing_of_eyes",
            [
                "yellowing of eyes",
                "yellow eyes",
                "aankhon ka peela hona",
                "आँखों का पीला होना",
                "आंखों का पीलापन",
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