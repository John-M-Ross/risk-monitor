import numpy as np
import pandas as pd
from typing import Dict, List, Optional

class FinancialDataAggregator:
    
    def __init__(self):
        self.assets = {
            "Apple": {"platform": "TradFi", "volatility": 0.25, "liquidity": 0.95, "regulatory": 1.0},
            "Microsoft": {"platform": "TradFi", "volatility": 0.22, "liquidity": 0.96, "regulatory": 1.0},
            "JP Morgan": {"platform": "TradFi", "volatility": 0.28, "liquidity": 0.92, "regulatory": 1.0},
            "Aave": {"platform": "DeFi", "volatility": 0.65, "liquidity": 0.70, "regulatory": 0.2},
            "Uniswap": {"platform": "DeFi", "volatility": 0.70, "liquidity": 0.75, "regulatory": 0.3},
            "Lido": {"platform": "DeFi", "volatility": 0.80, "liquidity": 0.65, "regulatory": 0.1},
            "PayPal": {"platform": "FinTech", "volatility": 0.35, "liquidity": 0.85, "regulatory": 0.9},
            "Block": {"platform": "FinTech", "volatility": 0.45, "liquidity": 0.82, "regulatory": 0.8},
            "Stripe": {"platform": "FinTech", "volatility": 0.30, "liquidity": 0.60, "regulatory": 0.85},
        }
    
    def fetch_asset_data(self, asset_name: str) -> Optional[Dict]:
        return self.assets.get(asset_name)
    
    def compute_features(self, asset_data: Dict) -> np.ndarray:
        return np.array([
            asset_data.get("volatility", 0.5),
            asset_data.get("liquidity", 0.5),
            asset_data.get("regulatory", 0.5),
        ])
    
    def compute_descriptive_stats(self, data: List[float]) -> Dict:
        if not data:
            return {}
        return {
            "mean": np.mean(data),
            "median": np.median(data),
            "std": np.std(data),
            "min": np.min(data),
            "max": np.max(data),
            "count": len(data)
        }
    
    def get_platform_statistics(self, platform: str) -> Dict:
        platform_assets = [a for a in self.assets.values() if a["platform"] == platform]
        if not platform_assets:
            return {}
        volatilities = [a["volatility"] for a in platform_assets]
        return {
            "platform": platform,
            "assets_count": len(platform_assets),
            "volatility_stats": self.compute_descriptive_stats(volatilities),
        }
    
    def compare_platforms(self) -> pd.DataFrame:
        comparison = []
        for platform in ["TradFi", "DeFi", "FinTech"]:
            stats = self.get_platform_statistics(platform)
            comparison.append({
                "Platform": platform,
                "Assets": stats.get("assets_count", 0),
                "Avg Volatility": stats.get("volatility_stats", {}).get("mean", 0),
                "Max Volatility": stats.get("volatility_stats", {}).get("max", 0),
            })
        return pd.DataFrame(comparison)
