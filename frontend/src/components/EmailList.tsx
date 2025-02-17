import { EmailResult } from "../types";
import { Button } from "react-bootstrap";

interface EmailListProps {
  results: EmailResult[];
  selectedEmail: EmailResult | null;
  onEmailClick: (email: EmailResult) => void;
  onEmailHover: (id: number | null) => void;
}

function EmailList({
  results,
  selectedEmail,
  onEmailClick,
  onEmailHover,
}: EmailListProps) {
  const scrollToTop = () => {
    const container = document.querySelector(".email-list-container");
    if (container) {
      container.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="position-relative" style={{ height: "80vh" }}>
      <div
        className="border rounded p-4 bg-white shadow-sm email-list-container"
        style={{ height: "calc(100% - 45px)", overflowY: "auto" }}
      >
        {results.map((email, index) => (
          <div
            id={`email-${email.id}`}
            key={email.id}
            className={`border-bottom ${
              selectedEmail === email ? "bg-light" : ""
            }`}
            style={{
              padding: "8px 6px",
              cursor: "pointer",
              transition: "background-color 0.15s ease-in-out",
            }}
            onClick={() => onEmailClick(email)}
            onMouseEnter={() => onEmailHover(index)}
            onMouseLeave={() => onEmailHover(null)}
          >
            <div
              className="fw-semibold mb-1"
              style={{
                fontSize: "1.05rem",
                lineHeight: "1.2",
                color: "#2c3e50",
              }}
            >
              {email.subject}
            </div>
            <div
              className="text-muted"
              style={{
                fontSize: "0.9rem",
              }}
            >
              From: {email.from}
            </div>
            <div className="text-muted" style={{ fontSize: "0.9rem" }}>
              {new Date(email.date).toLocaleDateString()}
            </div>
          </div>
        ))}
        {results.length === 0 && (
          <div className="text-center text-muted py-4"></div>
        )}
      </div>
      <Button
        onClick={scrollToTop}
        className="w-100 mt-2 d-flex align-items-center justify-content-center"
        variant="light"
        style={{ height: "40px" }}
      >
        ↑ Email List Top
      </Button>
    </div>
  );
}

export default EmailList;
