import sqlite3
import numpy as np
import json
from typing import List, Optional, Dict, Type
from documents import Document, Email


class DocumentStore:
    """
    SQLite-based storage for document objects and their vector embeddings.

    Handles persistence of Document objects and their computed vector embeddings,
    allowing for efficient storage and retrieval of processed documents. Supports
    different document types through a type mapping system.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initialize store with database path.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.type_map: Dict[str, Type[Document]] = {
            "Email": Email,
            "Document": Document,
        }
        self.init_db()

    def init_db(self) -> None:
        """
        Initialize database with required schema.

        Creates the documents table if it doesn't exist. Table stores:
        - Document ID
        - Document type (for proper reconstruction)
        - JSON-serialized document data
        - JSON-serialized vector embeddings
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                type TEXT,                 -- Document class name for reconstruction
                data TEXT,                 -- JSON-serialized document data
                vectors TEXT               -- JSON-serialized vector embeddings
            )
        """
        )

        conn.commit()
        conn.close()

    def save_document(self, doc_id: str, document: Document) -> None:
        """
        Save document and its vector embeddings to database.

        Args:
            doc_id: Unique identifier for the document
            document: Document instance to save

        Note:
            Replaces existing document if doc_id already exists
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Convert numpy arrays to lists for JSON serialization
        vectors_dict = document.to_vectors()
        vectors_serialized = {
            field: vec.tolist() for field, vec in vectors_dict.items()
        }

        c.execute(
            """
            INSERT OR REPLACE INTO documents (id, type, data, vectors)
            VALUES (?, ?, ?, ?)
        """,
            (
                doc_id,
                document.__class__.__name__,
                json.dumps(document.data),
                json.dumps(vectors_serialized),
            ),
        )

        conn.commit()
        conn.close()

    def load_document(self, doc_id: str) -> Optional[Document]:
        """
        Load a single document from database.

        Args:
            doc_id: Document identifier to load

        Returns:
            Reconstructed Document instance, or None if not found

        Note:
            Reconstructs the original document type (Email, etc.) based on
            stored type information
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("SELECT type, data, vectors FROM documents WHERE id = ?", (doc_id,))
        result = c.fetchone()
        conn.close()

        if result is None:
            return None

        doc_type, data, vectors = result
        data = json.loads(data)
        vectors = {field: np.array(vec) for field, vec in json.loads(vectors).items()}

        # Use type_map to create correct object type
        doc_class = self.type_map.get(doc_type)
        if doc_class:
            doc = doc_class(**data)
            doc._vectors = vectors
            return doc

        return None

    def load_all_documents(self) -> List[Document]:
        """
        Load all documents from database.

        Returns:
            List of all stored documents, reconstructed to their proper types
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute("SELECT id, type, data, vectors FROM documents")
        results = c.fetchall()
        conn.close()

        documents = []
        for doc_id, doc_type, data, vectors in results:
            data = json.loads(data)
            vectors = {
                field: np.array(vec) for field, vec in json.loads(vectors).items()
            }

            doc_class = self.type_map.get(doc_type)
            if doc_class:
                doc = doc_class(**data)
                doc._vectors = vectors
                documents.append(doc)

        return documents

    def clear_store(self) -> None:
        """
        Delete all documents from database.

        Useful for resetting the store or clearing cached data.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM documents")
        conn.commit()
        conn.close()
