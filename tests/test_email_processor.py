# tests/test_email_processor.py
import os
import sys
import pytest

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_dir)

from email_processor import EmailProcessor
from document_store import DocumentStore

class TestEmailProcessor:
    def test_process_mbox(self, temp_mbox, tmp_path):
        store = DocumentStore(str(tmp_path / "test.db"))
        processor = EmailProcessor(temp_mbox, store)
        emails = processor.process_mbox()
        
        assert len(emails) > 0
        assert emails[0].data['subject'] == 'Test Subject'

    def test_clean_whitespace(self, temp_mbox):
        store = DocumentStore("test.db")
        processor = EmailProcessor(temp_mbox, store)
        text = "Multiple    spaces\nand\nnewlines"
        cleaned = processor.clean_whitespace(text)
        assert cleaned == "Multiple spaces and newlines"

    def test_decode_email_subject(self, temp_mbox):
        store = DocumentStore("test.db")
        processor = EmailProcessor(temp_mbox, store)
        subject = "=?utf-8?q?Test=20Subject?="
        decoded = processor.decode_email_subject(subject)
        assert isinstance(decoded, str)