import os
import sys
import pytest

# Add backend directory to Python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_dir)

from document_store import DocumentStore

@pytest.fixture
def document_store(tmp_path):
    """Fixture to create and cleanup test database."""
    db_path = str(tmp_path / "test_documents.db")
    store = DocumentStore(db_path)
    return store

class TestDocumentStore:
    def test_save_and_load_document(self, document_store, sample_email):
        """Test basic save and load functionality."""
        document_store.save_document("test1", sample_email)
        loaded_doc = document_store.load_document("test1")
        
        assert loaded_doc is not None
        assert loaded_doc.data['subject'] == "Test Subject"
        assert type(loaded_doc).__name__ == "Email"
        
    def test_load_all_documents(self, document_store, sample_email):
        """Test loading multiple documents."""
        document_store.save_document("test1", sample_email)
        document_store.save_document("test2", sample_email)
        
        docs = document_store.load_all_documents()
        assert len(docs) == 2
        
    def test_clear_store(self, document_store, sample_email):
        """Test clearing all documents from store."""
        document_store.save_document("test1", sample_email)
        
        document_store.clear_store()
        docs = document_store.load_all_documents()
        assert len(docs) == 0