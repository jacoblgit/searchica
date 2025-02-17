import { Modal, Button } from "react-bootstrap";

interface TutorialModalProps {
  show: boolean;
  onHide: () => void;
}

const TutorialModal = ({ show, onHide }: TutorialModalProps) => {
  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Welcome to Searchica</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p className="mb-3">
          Searchica is a tool for exploring a corpus of documents through
          semantic search (finding results based on meaning rather than just
          keywords) and visualization. This site uses as an example a sample of
          Enron's C-suite emails from the FBI investigation into them.
        </p>
        <ul className="mt-3">
          <li className="mb-2">Enter your search query in the search bar. </li>
          <li className="mb-2">
            Points are plotted based on semantic meaning. Emails are colored and
            listed based on semantic similarity to the query (red, higher is
            better).
          </li>
          <li className="mb-2">
            Click on a point to highlight the email. Hover on an email to
            highlight a point. Click on an email to see its full text, and click
            again to close. Zoom in on a point to see related emails.
          </li>
          <li>
            For more information see:{" "}
            <a
              href="https://github.com/jacoblgit/searchica"
              target="_blank"
              rel="noopener noreferrer"
            >
              github.com/jacoblgit/searchica
            </a>
          </li>
        </ul>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={onHide}>
          Got it!
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default TutorialModal;
