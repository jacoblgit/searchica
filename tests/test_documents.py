# tests/test_documents.py
import os
import sys
import pytest
import numpy as np

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_dir)

from documents import Document, Email

class TestDocument:
    def test_document_initialization(self, sample_document):
        assert sample_document.data['field1'] == 'Content 1'
        assert sample_document._vectors is None
        assert isinstance(sample_document.field_weights, dict)

    def test_to_vectors(self, sample_document):
        vectors = sample_document.to_vectors()
        assert isinstance(vectors, dict)
        assert all(isinstance(v, np.ndarray) for v in vectors.values())

    def test_get_combined_vector(self, sample_document):
        sample_document.field_weights = {'field1': 0.6, 'field2': 0.4}
        combined = sample_document.get_combined_vector()
        assert isinstance(combined, np.ndarray)

class TestEmail:
    def test_email_initialization(self, sample_email):
        assert sample_email.data['subject'] == 'Test Subject'
        assert sample_email.data['body'] == 'Test email body content'
        assert sample_email.field_weights['body'] == 0.4
        assert sample_email.field_weights['subject'] == 0.3

    def test_email_vector_creation(self, sample_email):
        vectors = sample_email.to_vectors()
        assert 'body' in vectors
        assert 'subject' in vectors
        assert all(isinstance(v, np.ndarray) for v in vectors.values())

    def test_email_weights_sum(self, sample_email):
        weights_sum = sum(sample_email.field_weights.values())
        assert pytest.approx(weights_sum, 0.01) == 1.0