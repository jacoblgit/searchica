import mailbox
from bs4 import BeautifulSoup
import re
from typing import List, Optional
from email.header import decode_header
from documents import Email
from document_store import DocumentStore


class EmailProcessor:
    """
    Processes mbox files to extract email content and metadata for semantic search.

    Handles parsing of mbox format emails, extracting meaningful text content from
    both plain text and HTML formatted emails, and cleaning the extracted data.
    Processed emails are saved to a document store for later retrieval.
    """

    def __init__(self, mbox_path: str, doc_store: DocumentStore) -> None:
        """
        Initialize processor with mbox file path and document store.

        Args:
            mbox_path: Path to mbox file containing emails
            doc_store: DocumentStore instance for saving processed emails
        """
        self.mbox_path = mbox_path
        self.doc_store = doc_store

    def process_mbox(self) -> List[Email]:
        """
        Process all emails in the mbox file and save to document store.

        Extracts content and metadata from each email, converts to Email objects,
        and saves them to the document store. Handles errors for individual emails
        without failing the entire process.

        Returns:
            List of successfully processed Email objects

        Raises:
            FileNotFoundError: If mbox file doesn't exist
        """
        mbox = mailbox.mbox(self.mbox_path)
        processed_emails = []

        for i, message in enumerate(mbox):
            try:
                email = self.process_single_email(message)
                if email:
                    self.doc_store.save_document(f"email_{i}", email)
                    processed_emails.append(email)
            except Exception as e:
                print(
                    f"Error processing email with subject '{message['subject']}': {str(e)}"
                )

        return processed_emails

    def clean_whitespace(self, text: str) -> str:
        """
        Clean and normalize whitespace in text.

        Replaces multiple whitespace characters (including newlines) with single spaces
        and strips leading/trailing whitespace.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text with normalized whitespace
        """
        return re.sub(r"\s+", " ", text).strip()

    def process_single_email(self, message: mailbox.mboxMessage) -> Optional[Email]:
        """
        Extract content and metadata from a single email message.

        Processes both plain text and HTML formatted emails. For HTML emails,
        extracts meaningful text content from the DOM structure. Handles email
        header decoding and metadata extraction.

        Args:
            message: Email message from mbox file

        Returns:
            Email object with processed content and metadata, or None if processing fails

        Raises:
            ValueError: If no text content found in email
        """
        email_content = None
        content_type = None

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/html":
                    email_content = part.get_payload(decode=True).decode()
                    content_type = "html"
                    break
                elif part.get_content_type() == "text/plain":
                    email_content = part.get_payload(decode=True).decode()
                    content_type = "plain"
                    break
        else:
            email_content = message.get_payload(decode=True).decode()
            content_type = message.get_content_type()

        if not email_content:
            raise ValueError("No text content found")

        if content_type == "text/html":
            soup = BeautifulSoup(email_content, "html.parser")
            email_content = soup.get_text()

        email_content = self.clean_whitespace(email_content)
        subject_decoded = self.decode_email_subject(message["subject"])

        return Email(
            body=email_content,
            subject=subject_decoded,
            sender=message["from"],
            to=message["to"],
            cc=message["cc"],
            bcc=message["bcc"],
            date=message["date"],
        )

    @staticmethod
    def decode_email_subject(subject: Optional[str]) -> str:
        """
        Decode email subject header that may contain encoded character sets.

        Args:
            subject: Raw email subject header

        Returns:
            Decoded subject text, or empty string if subject is None
        """
        if not subject:
            return ""

        decoded_tuple = decode_header(subject)[0]
        decoded_text, encoding = decoded_tuple
        if isinstance(decoded_text, bytes):
            return decoded_text.decode(encoding or "utf-8")
        return decoded_text
