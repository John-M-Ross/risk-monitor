from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd

@dataclass
class RiskMemory:
    max_assets: int = 5
    asset_list: List[str] = field(default_factory=list)
    risk_results: List[Dict] = field(default_factory=list)
    
    def add_asset(self, asset: str, result: Dict) -> bool:
        if asset not in self.asset_list and len(self.asset_list) < self.max_assets:
            self.asset_list.append(asset)
            self.risk_results.append(result)
            return True
        return False
    
    def has_asset(self, asset: str) -> bool:
        return asset in self.asset_list
    
    def is_full(self) -> bool:
        return len(self.asset_list) >= self.max_assets
    
    def get_high_risk_assets(self, threshold: int = 70) -> List[Dict]:
        high_risk = []
        for asset, result in zip(self.asset_list, self.risk_results):
            if result.get("risk_score", 0) >= threshold:
                high_risk.append({"asset": asset, "risk_score": result["risk_score"], "risk_category": result["risk_category"]})
        return high_risk

class RiskMonitorAgent:
    def __init__(self, data_aggregator, risk_model):
        self.data_aggregator = data_aggregator
        self.risk_model = risk_model
        self.memory = None
    
    def _send_alert(self, high_risk_assets: List[Dict]) -> None:
        print(f"\n🚨 {len(high_risk_assets)} HIGH-RISK ALERTS 🚨")
        for asset in high_risk_assets:
            print(f"   🔴 {asset['asset']}: {asset['risk_score']}% ({asset['risk_category']})")
    
    def run(self, asset_list: List[str]) -> pd.DataFrame:
        print(f"\n{'='*50}")
        print(f"🤖 RISK MONITOR AGENT ACTIVE")
        print(f"{'='*50}")
        
        self.memory = RiskMemory(max_assets=5)
        results = []
        
        for asset in asset_list[:5]:
            if self.memory.has_asset(asset):
                continue
            
            asset_data = self.data_aggregator.fetch_asset_data(asset)
            if not asset_data:
                continue
            
            features = self.data_aggregator.compute_features(asset_data)
            risk_result = self.risk_model.predict_risk(features)
            self.memory.add_asset(asset, risk_result)
            
            results.append({
                "Asset": asset,
                "Platform": asset_data["platform"],
                "Risk Score": risk_result["risk_score"],
                "Risk Category": risk_result["risk_category"],
                "Volatility": asset_data.get("volatility", 0),
                "Liquidity": asset_data.get("liquidity", 0),
                "Regulatory": asset_data.get("regulatory", 0),
            })
        
        high_risk = self.memory.get_high_risk_assets()
        if high_risk:
            self._send_alert(high_risk)
        
        return pd.DataFrame(results)
