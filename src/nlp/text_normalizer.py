"""
RuralCare AI
Text Normalizer

Responsible for:
- Lowercasing
- Removing punctuation
- Normalizing spaces
- Unicode normalization
"""

import re
import unicodedata


class TextNormalizer:

    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""

        # Unicode normalization
        text = unicodedata.normalize("NFKC", text)

        # Lowercase
        text = text.lower()

        # Replace punctuation/symbols with spaces, but keep letters,
        # digits, and combining marks. Devanagari (and many other
        # scripts) build syllables from a base consonant plus combining
        # vowel signs/nukta (Unicode category Mn) - e.g. "बुखार" is
        # "ब" + "ु" + "ख" + "ा" + "र". Python's regex \w does NOT
        # include those combining marks, so `[^\w\s]` was silently
        # stripping them and shredding every Hindi word into
        # disconnected consonants (e.g. "मरीज़" -> "मर ज") before any
        # symptom matching could run. Category-based filtering (L =
        # Letter, M = Mark, N = Number) keeps the syllables intact.
        text = "".join(
            ch if ch.isspace() or unicodedata.category(ch)[0] in ("L", "M", "N")
            else " "
            for ch in text
        )

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()