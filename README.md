# Searchica

## Vision

The aim of this project is to enable efficient exploration of a corpus of documents through semantic search and visualization.

## Implementation

Currently, Searchica only supports email archives in an mbox format. The semantic search implementation is BERT embeddings. The stack is Flask/React.
There are sample emails that can be used for testing, retrieved from the public release of enron emails.

### Core Components

#### Vector Embedding System

- Utilizes `msmarco-MiniLM-L6-cos-v5` BERT model
- Implements lazy loading pattern for vector computation
- Caches embeddings in SQLite with JSON serialization

#### Search Implementation

- Cosine similarity computation between query and document vectors
- Weighted field scoring across email components
- Result ranking based on similarity score

#### Visualization processing

- PCA dimensionality reduction for visualization mapping
- Normalized score used to color nodes on plot
- Plotly data structure generation

##### Frontend (React)

- Search interface
- Plotly.js visualization integration
- REST API integration

#### Data Pipeline

- Email parsing (mbox format)
- Content extraction from plain text and HTML
- Vector embedding computation
- SQLite storage with vector caching
- Query processing and similarity scoring
- 2D projection for visualization

#### Testing

Pytest suite covering:

- Document vector operations
- Email parsing and storage
- Search functionality
- Visualization processing

### Setup

```bash
git clone [repository]
pip install -r requirements.txt
```

```bash
# For production

# Build frontend
cd frontend
npm run build

# Start backend
$env:FLASK_ENV = "production"
cd backend
python app.py
```

```bash
# For development

# Start frontend
cd frontend
npm run dev

# Start backend
$env:FLASK_ENV = ""
cd backend
python app.py
```

```bash
# For deployment (Docker)

# Build frontend
cd frontend
npm run build

# Build Docker
docker build -t searchica .

# Deploy to Google Cloud
docker tag searchica [full Google artifact registry address]:latest
docker push [full Google artifact registry address]:latest
# update Google Cloud Run image to be newly uploaded Docker container 
```
