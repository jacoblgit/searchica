from typing import Dict, Optional, Any
from sentence_transformers import SentenceTransformer
import numpy as np


class Document:
    """
    Base document class that handles vector embeddings for semantic search.

    Converts document fields into vector embeddings using a BERT-based transformer
    model. Supports weighted combinations of field vectors for similarity scoring.
    Uses lazy loading to compute vectors only when needed.
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

    def __init__(self, data: Dict[str, Optional[str]]) -> None:
        """
        Initialize document with field data.

        Args:
            data: Dictionary of field names to content strings
        """
        self.data = data
        self._vectors: Optional[Dict[str, np.ndarray]] = None
        self.field_weights: Dict[str, float] = {}

    def to_vectors(self) -> Dict[str, np.ndarray]:
        """
        Convert each text field to its vector embedding.

        Uses lazy loading - vectors are computed only on first request
        and cached for subsequent uses.

        Returns:
            Dictionary mapping field names to their vector embeddings
        """
        if self._vectors is None:
            self._vectors = {}
            for field, value in self.data.items():
                if value is not None:
                    self._vectors[field] = self.get_model().encode(str(value))
        return self._vectors

    def get_combined_vector(self) -> np.ndarray:
        """
        Get single weighted vector representation of document.

        Combines vector embeddings of all fields using their weights.
        Fields without specified weights are ignored.

        Returns:
            Combined vector embedding for the entire document
        """
        vectors = self.to_vectors()
        combined = np.zeros_like(list(vectors.values())[0])
        for field, vector in vectors.items():
            weight = self.field_weights.get(field, 0)
            combined += weight * vector
        return combined


class Email(Document):
    """
    Email document type with predefined fields and weights.

    Extends Document class with email-specific fields and weightings
    for semantic similarity scoring. Weights determine relative importance
    of different email fields (subject, body, etc.) in search.
    """

    def __init__(
        self,
        body: str,
        subject: str,
        sender: str,
        to: str,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        date: Optional[str] = None,
    ) -> None:
        """
        Initialize email with content and metadata.

        Args:
            body: Main email content
            subject: Email subject line
            sender: Email sender
            to: Primary recipients
            cc: Carbon copy recipients
            bcc: Blind carbon copy recipients
            date: Email date
        """
        data = {
            "body": body,
            "subject": subject,
            "sender": sender,
            "to": to,
            "cc": cc,
            "bcc": bcc,
            "date": date,
        }
        super().__init__(data)

        # Define relative importance of each field for similarity scoring
        self.field_weights = {
            "subject": 0.3,  # Subject highly relevant for matching
            "body": 0.4,  # Body content most important
            "sender": 0.1,  # Sender moderately relevant
            "to": 0.1,  # Recipients moderately relevant
            "cc": 0.05,  # CC less important
            "bcc": 0.025,  # BCC minimal importance
            "date": 0.025,  # Date minimal importance
        }
