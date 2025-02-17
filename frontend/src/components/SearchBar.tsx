// SearchBar.tsx
import { Row, Col, Button } from "react-bootstrap";
import { useState } from "react";

interface SearchProps {
  onSearch: (query: string) => void;
  initialQuery?: string;
}

function SearchBar({ onSearch, initialQuery = "" }: SearchProps) {
  const [query, setQuery] = useState(initialQuery);

  const handleSearch = () => {
    onSearch(query);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <Row className="my-1">
      <Col>
        <div className="d-flex">
          <input
            type="text"
            className="form-control"
            placeholder="Search..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <Button variant="primary" className="ms-2" onClick={handleSearch}>
            Search
          </Button>
        </div>
      </Col>
    </Row>
  );
}

export default SearchBar;
