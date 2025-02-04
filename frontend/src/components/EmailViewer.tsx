import { EmailResult } from "../types";

interface EmailViewerProps {
  email: EmailResult;
}

function EmailViewer({ email }: EmailViewerProps) {
  return (
    <div
      className="border rounded p-4 bg-white shadow-sm"
      style={{ height: "80vh", overflowY: "auto" }}
    >
      <div className="mb-4">
        <h3>{email.subject}</h3>
        <div className="text-muted mb-2">
          <div>From: {email.from}</div>
          <div>To: {email.to}</div>
          {email.cc && <div>CC: {email.cc}</div>}
          <div>Date: {new Date(email.date).toLocaleString()}</div>
        </div>
        <div style={{ whiteSpace: "pre-wrap" }}>{email.body}</div>
      </div>
    </div>
  );
}

export default EmailViewer;
