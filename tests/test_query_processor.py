# tests/test_query_processor.py
import os
import sys
import pytest
import numpy as np

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_dir)

from query_processor import QueryProcessor

class TestQueryProcessor:
    def test_search(self, sample_email):
        processor = QueryProcessor([sample_email])
        results = processor.search("test", top_k=1)
        
        assert len(results) == 1
        assert results[0][0] == sample_email

    def test_compute_similarity(self, sample_email):
        processor = QueryProcessor([sample_email])
        query_vector = processor.get_model().encode("test query")
        similarity = processor.compute_similarity(query_vector, sample_email)
        
        assert -1 <= similarity <= 1  # Cosine similarity bounds

    def test_cosine_similarity(self):
        v1 = np.array([1, 0, 0])
        v2 = np.array([0, 1, 0])
        similarity = QueryProcessor.cosine_similarity(v1, v2)
        assert similarity == 0  # Orthogonal vectors