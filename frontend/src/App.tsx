import { Container, Row, Col } from "react-bootstrap";
import { useState } from "react";
import { EmailResult, PlotData, Trace, Marker } from "./types";
import SearchBar from "./components/SearchBar";
import VisualizationPanel from "./components/VisualizationPanel";
import EmailList from "./components/EmailList";
import EmailViewer from "./components/EmailViewer";
import Footer from "./components/Footer";
import Logo from "./components/Logo";

function App() {
  const [plotData, setPlotData] = useState<PlotData | null>(null);
  const [emailResults, setEmailResults] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState<EmailResult | null>(null);
  const [hoveredId, setHoveredId] = useState<number | null>(null);

  const handleEmailHover = (id: number | null) => {
    setHoveredId(id);
    console.log(id);
  };

  const handlePointClick = (pointIndex: number) => {
    const email = emailResults[pointIndex];
    const element = document.getElementById(`email-${pointIndex}`);
    element?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const handleSearch = async (query: string) => {
    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setPlotData(data.plot_data);
      setEmailResults(data.results);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  const handleEmailClick = (email: EmailResult) => {
    if (selectedEmail === email) {
      // If clicking the currently selected email, deselect it
      setSelectedEmail(null);
    } else {
      // Otherwise, select the new email
      setSelectedEmail(email);
    }
  };

  return (
    <div style={{ backgroundColor: "#f8f9fa", minHeight: "100vh" }}>
      <Container
        fluid
        style={{ maxWidth: "1400px", margin: "0 auto", padding: "20px" }}
      >
        <Row className="mt-1 mb-4">
          {" "}
          {/* increased from my-3 */}
          <Col>
            <div className="d-flex align-items-center bg-white rounded p-4 shadow-sm">
              {" "}
              {/* added padding and shadow */}
              <Logo />
              <div style={{ width: "100%" }}>
                <SearchBar onSearch={handleSearch} />
              </div>
            </div>
          </Col>
        </Row>
        <Row>
          <Col lg={8}>
            {selectedEmail ? (
              <EmailViewer email={selectedEmail} />
            ) : (
              <VisualizationPanel
                plotData={plotData}
                onPointClick={handlePointClick}
                hoveredId={hoveredId}
              />
            )}
          </Col>
          <Col lg={4}>
            <EmailList
              results={emailResults}
              selectedEmail={selectedEmail}
              onEmailClick={handleEmailClick}
              onEmailHover={handleEmailHover}
            />
          </Col>
        </Row>
        <Footer />
      </Container>
    </div>
  );
}

export default App;
