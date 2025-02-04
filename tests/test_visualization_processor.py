# tests/test_visualization_processor.py
import os
import sys
import pytest
import numpy as np

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_dir)

from visualization_processor import VisualizationProcessor

class TestVisualizationProcessor:
    def test_initialization(self, sample_email):
        doc_scores = [(sample_email, 0.8), (sample_email, 0.6)]
        processor = VisualizationProcessor(doc_scores)

    def test_exp_normalize(self):
        scores = np.array([0.5, 0.8, 0.2])
        normalized = VisualizationProcessor.exp_normalize(scores, alpha=0.1, beta=10)
        
        assert all(0 <= score <= 1 for score in normalized)
        assert len(normalized) == len(scores)

    def test_get_node_color(self):
        color = VisualizationProcessor.get_node_color(0.5)
        assert color.startswith('rgb(')
        assert color.endswith(')')