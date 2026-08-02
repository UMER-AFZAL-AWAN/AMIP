import numpy as np
import hdbscan
import joblib
import os
from typing import Tuple

class PatternClustering:
    def __init__(self, min_cluster_size: int = 15, min_samples: int = 5):
        self.clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, 
                                         min_samples=min_samples, 
                                         prediction_data=True)
        
    def fit(self, embeddings: np.ndarray) -> np.ndarray:
        self.clusterer.fit(embeddings)
        return self.clusterer.labels_
        
    def predict(self, embeddings: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        labels, strengths = hdbscan.approximate_predict(self.clusterer, embeddings)
        return labels, strengths
        
    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.clusterer, filepath)
        
    def load(self, filepath: str):
        self.clusterer = joblib.load(filepath)
