from typing import List, Dict, Optional, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from documents import Document


class QueryProcessor:
    """
    Handles semantic search queries across a collection of documents using BERT embeddings.

    Uses a sentence transformer model to convert text queries into vector space,
    then computes similarity scores with document embeddings to find the most relevant matches.
    The model is optimized for cosine similarity and shorter passages.
    """

    _shared_model: Optional[SentenceTransformer] = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        """
        Get or initialize the shared transformer model singleton.

        Returns:
            SentenceTransformer: Instance of msmarco-MiniLM-L6-cos-v5 model,
                                optimized for fast encoding and cosine similarity
        """
        if cls._shared_model is None:
            cls._shared_model = SentenceTransformer(
                "sentence-transformers/msmarco-MiniLM-L6-cos-v5"
            )
        return cls._shared_model

    def __init__(self, documents: List[Document]) -> None:
        """
        Initialize processor with collection of documents to search.

        Args:
            documents: List of Document objects to include in search
        """
        self.documents = documents

    def search(
        self, query: str, top_k: Optional[int] = None
    ) -> List[Tuple[Document, float]]:
        """
        Search documents for matches to query text.

        Encodes query text into vector space and computes similarity scores
        with all documents. Returns documents sorted by relevance score.

        Args:
            query: Search query text
            top_k: Optional limit on number of results to return

        Returns:
            List of (Document, score) tuples sorted by descending score
        """
        query_vector = self.get_model().encode(query)
        scored_docs = [
            (doc, self.compute_similarity(query_vector, doc)) for doc in self.documents
        ]
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:top_k] if top_k is not None else scored_docs

    def compute_similarity(self, query_vector: np.ndarray, doc: Document) -> float:
        """
        Compute similarity score between query vector and document.

        Args:
            query_vector: Encoded query vector
            doc: Document to compare against

        Returns:
            Cosine similarity score between query and document vectors
        """
        doc_vector = doc.get_combined_vector()
        return self.cosine_similarity(query_vector, doc_vector)

    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors.

        Args:
            v1: First vector
            v2: Second vector

        Returns:
            Cosine similarity score between -1 and 1
        """
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
