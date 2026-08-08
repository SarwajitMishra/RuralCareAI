"""
============================================================
RuralCareAI
Fuzzy Symptom Matcher
============================================================
"""

from rapidfuzz import process, fuzz


class FuzzyMatcher:

    def __init__(self, dictionary):

        self.dictionary = dictionary

        self.aliases = list(
            dictionary.get_all_aliases().keys()
        )

    def match(self, word, threshold=85):

        if not word:
            return None

        result = process.extractOne(
            word.lower(),
            self.aliases,
            scorer=fuzz.ratio
        )

        if result is None:
            return None

        matched_word, score, _ = result

        if score < threshold:
            return None

        return self.dictionary.lookup_alias(
            matched_word
        )