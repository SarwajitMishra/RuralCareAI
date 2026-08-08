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

        # Replace punctuation with spaces
        text = re.sub(r"[^\w\s]", " ", text)

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()