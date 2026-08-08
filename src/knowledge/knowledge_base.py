"""
Offline Healthcare Knowledge Retrieval (RAG) for RuralCareAI.

Wraps a local, persistent ChromaDB vector store over the structured
healthcare knowledge repository so the predicted disease can be
grounded with retrieved, verified context before being passed to
the Local LLM for clinical summary generation.

Author: Sarwajit Kumar Mishra
"""

from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

from src.knowledge.data import DISEASE_KNOWLEDGE, get_disease_knowledge

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"
COLLECTION_NAME = "healthcare_knowledge"


def _document_text(disease: str, entry: dict) -> str:
    parts = [
        disease,
        entry.get("description", ""),
        "Precautions: " + "; ".join(entry.get("precautions", [])),
        "First aid: " + "; ".join(entry.get("first_aid", [])),
        "When to consult a doctor: " + entry.get("when_to_consult", ""),
        "Emergency warning signs: " + "; ".join(entry.get("emergency_signs", [])),
    ]
    return "\n".join(parts)


class KnowledgeBase:
    """
    Local semantic retrieval over the offline healthcare knowledge repository.
    """

    def __init__(self):
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))

        self.embedding_function = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_function,
        )

        self._build_index()

    # --------------------------------------------------------------
    # Index construction (idempotent)
    # --------------------------------------------------------------

    def _build_index(self):
        if self.collection.count() >= len(DISEASE_KNOWLEDGE):
            return

        ids = list(DISEASE_KNOWLEDGE.keys())

        documents = [
            _document_text(disease, entry)
            for disease, entry in DISEASE_KNOWLEDGE.items()
        ]

        self.collection.upsert(ids=ids, documents=documents)

    # --------------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------------

    def retrieve(self, disease: str) -> dict:
        """
        Retrieve the structured knowledge entry most relevant to the
        predicted disease using semantic similarity search.

        Falls back to the generic default entry if retrieval fails
        or the store is empty.
        """

        if disease in DISEASE_KNOWLEDGE:
            return {"disease": disease, **DISEASE_KNOWLEDGE[disease]}

        try:
            result = self.collection.query(query_texts=[disease], n_results=1)

            matched_ids = result.get("ids", [[]])[0]

            if matched_ids:
                matched_disease = matched_ids[0]
                return {
                    "disease": matched_disease,
                    **get_disease_knowledge(matched_disease),
                }

        except Exception:
            pass

        return {"disease": disease, **get_disease_knowledge(disease)}
