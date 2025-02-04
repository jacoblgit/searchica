from typing import List, Tuple, Dict, Any
import numpy as np
from sklearn.decomposition import PCA
from documents import Document


class VisualizationProcessor:
    """
    Processes document embeddings for 2D visualization using PCA dimensionality reduction.

    Handles the transformation of high-dimensional document vectors into 2D space,
    and prepares the data for visualization with custom coloring based on relevance scores.
    The visualization uses PCA to create a 2D scatter plot where similar documents
    appear closer together.
    """

    _shared_pca_embeddings: np.ndarray = None
    _shared_doc_vectors: np.ndarray = None

    def __init__(self, doc_scores: List[Tuple[Document, float]]) -> None:
        """
        Initialize processor with document-score pairs and compute 2D embeddings.

        Args:
            doc_scores: List of tuples containing (Document, similarity_score) pairs
        """
        self.doc_scores = doc_scores
        self.documents = [doc for doc, _ in doc_scores]
        self.scores = [score for _, score in doc_scores]

        # Compute 2D embeddings using PCA
        doc_vectors = np.array([doc.get_combined_vector() for doc in self.documents])
        pca = PCA(n_components=2, random_state=42)
        self.embeddings_2d = pca.fit_transform(doc_vectors)

    @staticmethod
    def exp_normalize(scores: np.ndarray, alpha: float, beta: float) -> np.ndarray:
        """
        Normalize scores using exponential function for visualization scaling.

        Args:
            scores: Raw similarity scores to normalize
            alpha: Scaling factor for the exponential function
            beta: Base multiplier in the exponential function

        Returns:
            Array of normalized scores between 0 and 1
        """
        normalized = alpha * np.exp(beta * scores)
        return np.minimum(normalized, 1)

    @staticmethod
    def get_node_color(normalized_score: float) -> str:
        """
        Convert normalized score to RGB color string for visualization.

        Creates a color gradient from blue (low score) to red (high score).

        Args:
            normalized_score: Score between 0 and 1

        Returns:
            RGB color string in format 'rgb(R,G,B)'
        """
        return f"rgb({int(255*normalized_score)}, 0, {int(255*(1-normalized_score))})"

    def prepare_visualization_data(self) -> Dict[str, Any]:
        """
        Prepare document embeddings and metadata for Plotly visualization.

        Transforms document vectors into 2D space and adds visual properties
        like colors and opacities based on similarity scores. Creates a complete
        data structure ready for Plotly scatter plot visualization.

        Returns:
            Dictionary containing Plotly trace and layout configurations:
            {
                'data': [trace],
                'layout': layout
            }
        """
        similarity_scores = np.array(self.scores)

        normalized_scores_color = self.exp_normalize(
            similarity_scores, alpha=0.1, beta=10
        )
        colors = [self.get_node_color(score) for score in normalized_scores_color]

        normalized_scores_opacity = self.exp_normalize(
            similarity_scores, alpha=0.1, beta=10
        )
        opacities = normalized_scores_opacity.tolist()

        trace = {
            "x": self.embeddings_2d[:, 0].tolist(),
            "y": self.embeddings_2d[:, 1].tolist(),
            "mode": "markers",
            "type": "scatter",
            "marker": {"color": colors, "size": 10, "opacity": opacities},
            "hovertext": [
                f"Match rank: {idx+1}<br>"
                f"{str(doc.data.get('subject', ''))[:50]}...<br>"
                f"From: {str(doc.data.get('sender', '')).split('<')[0]}"
                for idx, (doc, score) in enumerate(self.doc_scores)
            ],
            "hoverinfo": "text",
        }

        layout = {
            "showlegend": False,
            "hovermode": "closest",
            "xaxis": {"showgrid": False, "showticklabels": False, "zeroline": False},
            "yaxis": {"showgrid": False, "showticklabels": False, "zeroline": False},
            "plot_bgcolor": "white",
        }

        return {"data": [trace], "layout": layout}
