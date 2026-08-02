import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple, List

class PatternSimilarity:
    def __init__(self):
        self.history_embeddings = None
        self.history_labels = None
        self.history_returns = None
        
    def fit(self, embeddings: np.ndarray, labels: np.ndarray = None, returns: np.ndarray = None):
        self.history_embeddings = embeddings
        self.history_labels = labels
        self.history_returns = returns
        
    def find_similar(self, query_embedding: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """Find top_k most similar historical patterns."""
        if self.history_embeddings is None:
            raise ValueError("History is empty. Call fit() first.")
            
        # Ensure 2D
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
            
        sims = cosine_similarity(query_embedding, self.history_embeddings)[0]
        top_indices = np.argsort(sims)[::-1][:top_k]
        top_sims = sims[top_indices]
        
        return top_indices, top_sims
        
    def get_historical_outcomes(self, indices: np.ndarray) -> dict:
        """Get the historical returns and labels for given indices."""
        outcomes = {}
        if self.history_labels is not None:
            outcomes['labels'] = self.history_labels[indices]
        if self.history_returns is not None:
            outcomes['returns'] = self.history_returns[indices]
            
        return outcomes
