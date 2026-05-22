import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Dict

class RiskScoringModel:
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.risk_categories = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk", 3: "Critical Risk"}
        self.risk_scores = {0: 20, 1: 50, 2: 75, 3: 95}
    
    def train(self) -> float:
        X = np.array([
            [0.2, 0.9, 0.9], [0.4, 0.8, 0.7], [0.5, 0.7, 0.5],
            [0.6, 0.5, 0.4], [0.7, 0.4, 0.3], [0.8, 0.3, 0.2], [0.9, 0.2, 0.1],
        ])
        X_scaled = self.scaler.fit_transform(X)
        self.model = KMeans(n_clusters=4, random_state=42, n_init=10)
        self.model.fit(X_scaled)
        silhouette = silhouette_score(X_scaled, self.model.labels_)
        print(f"Risk model trained. Silhouette Score: {silhouette:.4f}")
        return silhouette
    
    def predict_risk(self, features: np.ndarray) -> Dict:
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        cluster = self.model.predict(features_scaled)[0]
        return {
            "risk_category": self.risk_categories[cluster],
            "risk_score": self.risk_scores[cluster],
            "cluster": cluster
        }
