import { Row, Col } from "react-bootstrap";

function Footer() {
  return (
    <Row className="mt-3">
      <Col className="text-center text-muted small">
        © 2024 Jacob Lessing &middot;{" "}
        <a
          href="https://jacoblessing.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          jacoblessing.com
        </a>
      </Col>
    </Row>
  );
}

export default Footer;
