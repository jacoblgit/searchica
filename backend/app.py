from waitress import serve
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
from typing import List, Dict, Any, Optional
from pathlib import Path
import os

from email_processor import EmailProcessor
from document_store import DocumentStore
from query_processor import QueryProcessor
from visualization_processor import VisualizationProcessor
from documents import Document

# Environment-based configuration
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
IS_DEVELOPMENT = ENVIRONMENT == 'development'

# Default configuration
DEFAULT_CONFIG = {
    "MBOX_PATH": Path("../data/mbox-enron-white-s-all.mbox"),
    "STORE_PATH": Path("../data/processed_doc_cache.db"),
    "STATIC_FOLDER": Path("dist") if not IS_DEVELOPMENT else None
}

class SearchicaApp:
    """
    Flask application for semantic email search and visualization.

    Provides a REST API for searching and visualizing email content using
    semantic similarity. Handles document processing, search queries, and
    visualization preparation.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize application with configuration.

        Args:
            config: Optional configuration dictionary to override defaults
        """
        self.config = DEFAULT_CONFIG.copy()
        if config:
            self.config.update(config)

        if IS_DEVELOPMENT:
            self.app = Flask(__name__)
            CORS(self.app)
        else:
            self.app = Flask(__name__, static_folder=str(self.config["STATIC_FOLDER"]))
        
        # Initialize document processing
        self.doc_list = self.init_documents(
            self.config["MBOX_PATH"],
            self.config["STORE_PATH"],
            force_reprocess=False
        )

        # Initialize query processor
        self.query_processor = QueryProcessor(self.doc_list)

        # Register routes
        self.register_routes()

    def init_documents(
        self, mbox_path: Path, store_path: Path, force_reprocess: bool = False
    ) -> List[Document]:
        """
        Initialize document store and process emails.

        Loads processed documents from cache if available, otherwise processes
        raw emails from mbox file.

        Args:
            mbox_path: Path to mbox file containing emails
            store_path: Path to document store database
            force_reprocess: If True, reprocess emails even if cache exists

        Returns:
            List of processed documents
        """
        doc_store = DocumentStore(str(store_path))

        if not force_reprocess:
            emails = doc_store.load_all_documents()
            if emails:
                print("Loaded emails from store")
                return emails

        print("Starting processing emails from mbox")
        doc_store.clear_store()
        processor = EmailProcessor(str(mbox_path), doc_store)
        emails = processor.process_mbox()
        print("Finished processing emails from mbox")
        return emails

    def register_routes(self) -> None:
        """Register Flask route handlers."""

        @self.app.route("/api/status")
        def status() -> Dict[str, str]:
            """
            Home endpoint returning API status.

            Returns:
                Dictionary with API status information
            """
            return jsonify({"status": "running",
                            "version": "1.0",
                            "api": "searchica",
                            "environment": ENVIRONMENT})

        @self.app.route("/api/search", methods=["POST"])
        def search() -> Dict[str, Any]:
            """
            Search endpoint handling semantic search queries.

            Expects JSON request with 'query' field.
            Returns search results and visualization data.

            Returns:
                Dictionary containing:
                - plot_data: Visualization data for Plotly
                - results: List of matched documents with metadata
            """
            query = request.json.get("query", "")
            results = self.query_processor.search(query)

            viz_processor = VisualizationProcessor(results)
            plot_data = viz_processor.prepare_visualization_data()

            return jsonify(
                {
                    "plot_data": plot_data,
                    "results": [
                        {
                            "id": idx,
                            "subject": doc.data.get("subject"),
                            "from": doc.data.get("sender", "").split("<")[0],
                            "date": doc.data.get("date"),
                            "body": doc.data.get("body"),
                            "to": doc.data.get("to"),
                            "cc": doc.data.get("cc"),
                            "score": score,
                        }
                        for idx, (doc, score) in enumerate(results)
                    ],
                }
            )

        if not IS_DEVELOPMENT:
            @self.app.route('/')
            def serve_root():
                """Serve the static React app"""
                return send_from_directory(self.app.static_folder, 'index.html')
            
            @self.app.route('/<path:path>')
            def catch_all(path):
                """Redirect everything else to root"""
                return redirect('/')

    # def run(self, **kwargs) -> None:
    #     """Run the Flask application."""

    #     port = int(os.getenv('PORT', 5000))

    #     if IS_DEVELOPMENT:
    #         kwargs.setdefault('debug', True)
    #         kwargs.setdefault('host', 'localhost')
    #     else:
    #         kwargs['debug'] = False
    #         kwargs['host'] = '0.0.0.0'
        
    #     kwargs['port'] = port
    #     self.app.run(**kwargs)

app = SearchicaApp()
application = app.app  # This exposes the Flask instance for Gunicorn

if __name__ == "__main__":
    # app.run()
    port = int(os.getenv('PORT', 5000))

    if IS_DEVELOPMENT:
        host = 'localhost'
    else:
        host = '0.0.0.0'
    
    print(f"Running on {host}:{port} (localhost:{port} for local testing)")
    serve(application, host=host, port=port)