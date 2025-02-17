import { Container, Row, Col } from "react-bootstrap";
import { useState, useEffect } from "react";
import { EmailResult, PlotData, Trace, Marker } from "./types";
import SearchBar from "./components/SearchBar";
import VisualizationPanel from "./components/VisualizationPanel";
import EmailList from "./components/EmailList";
import EmailViewer from "./components/EmailViewer";
import Footer from "./components/Footer";
import Logo from "./components/Logo";
import TutorialModal from "./components/TutorialModal";

function App() {
  const [plotData, setPlotData] = useState<PlotData | null>(null);
  const [emailResults, setEmailResults] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState<EmailResult | null>(null);
  const [hoveredId, setHoveredId] = useState<number | null>(null);
  const [showTutorial, setShowTutorial] = useState(true);

  const handleEmailHover = (id: number | null) => {
    setHoveredId(id);
    console.log(id);
  };

  const handlePointClick = (pointIndex: number) => {
    const email = emailResults[pointIndex];
    const element = document.getElementById(`email-${pointIndex}`);
    element?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const exampleQuery = "evidence of criminal activity";
  useEffect(() => {
    // Call handleSearch with the example query when component mounts
    handleSearch(exampleQuery);
  }, []);

  const handleSearch = async (query: string) => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || "";
      console.log("Using API URL:", `${apiUrl}/api/search`);
      const response = await fetch(`${apiUrl}/api/search`, {
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
      <TutorialModal
        show={showTutorial}
        onHide={() => setShowTutorial(false)}
      />
      <Container
        fluid
        style={{ maxWidth: "1400px", margin: "0 auto", padding: "20px" }}
      >
        <Row className="mt-1 mb-4">
          {" "}
          <Col>
            <div className="d-flex align-items-center bg-white rounded p-4 shadow-sm">
              {" "}
              <Logo />
              <div style={{ width: "100%" }}>
                <SearchBar
                  onSearch={handleSearch}
                  initialQuery={exampleQuery}
                />
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
