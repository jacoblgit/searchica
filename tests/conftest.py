# tests/conftest.py
import os
import sys
import pytest
import numpy as np

# Add backend directory to Python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_dir)

from documents import Email, Document

@pytest.fixture
def sample_email():
    """Fixture providing a sample email for testing."""
    return Email(
        body="Test email body content",
        subject="Test Subject",
        sender="sender@example.com",
        to="recipient@example.com",
        cc="cc@example.com",
        bcc="bcc@example.com",
        date="2024-02-03"
    )

@pytest.fixture
def sample_document():
    """Fixture providing a sample document for testing."""
    return Document({
        'field1': 'Content 1',
        'field2': 'Content 2'
    })

@pytest.fixture
def mock_vectors():
    """Fixture providing sample vector embeddings."""
    return {
        'field1': np.array([0.1, 0.2, 0.3]),
        'field2': np.array([0.4, 0.5, 0.6])
    }

@pytest.fixture
def temp_mbox(tmp_path):
    """Fixture creating a temporary mbox file for testing."""
    mbox_content = """From sender@example.com Thu Feb 03 10:00:00 2024
Subject: Test Subject
From: sender@example.com
To: recipient@example.com
Date: Thu, 03 Feb 2024 10:00:00 -0000

Test email body content
"""
    mbox_file = tmp_path / "test.mbox"
    mbox_file.write_text(mbox_content)
    return str(mbox_file)