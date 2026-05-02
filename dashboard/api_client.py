"""
API Client for connecting to the FastAPI backend
Supports both local development and production deployment
"""

import os
import requests
import pandas as pd
from typing import Optional, Dict, Any
import streamlit as st

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

class ProcurementAPIClient:
    """Client for interacting with the Procurement Intelligence API"""
    
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_orders(self, **filters) -> pd.DataFrame:
        """Get procurement orders with optional filters"""
        params = {k: v for k, v in filters.items() if v is not None}
        response = self.session.get(f"{self.base_url}/orders", params=params, timeout=30)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    
    def get_filter_options(self) -> Dict[str, list]:
        """Get available filter options"""
        response = self.session.get(f"{self.base_url}/filters/options", timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_kpis(self) -> Dict[str, Any]:
        """Get key performance indicators"""
        response = self.session.get(f"{self.base_url}/kpis", timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics"""
        response = self.session.get(f"{self.base_url}/metrics", timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_forecast(self, periods: int = 12, confidence_level: float = 0.95) -> Dict[str, Any]:
        """Get spending forecast"""
        payload = {
            "periods": periods,
            "confidence_level": confidence_level
        }
        response = self.session.post(
            f"{self.base_url}/analytics/forecast", 
            json=payload, 
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_supplier_performance(self) -> Dict[str, Any]:
        """Get supplier performance analysis"""
        response = self.session.get(f"{self.base_url}/analytics/suppliers", timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_risk_assessment(self) -> Dict[str, Any]:
        """Get risk assessment"""
        response = self.session.get(f"{self.base_url}/analytics/risks", timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_optimization_opportunities(self) -> Dict[str, Any]:
        """Get optimization opportunities"""
        response = self.session.get(f"{self.base_url}/analytics/opportunities", timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_insights(self) -> Dict[str, Any]:
        """Get comprehensive insights"""
        response = self.session.get(f"{self.base_url}/analytics/insights", timeout=30)
        response.raise_for_status()
        return response.json()

# Create singleton client instance
@st.cache_resource
def get_api_client() -> ProcurementAPIClient:
    """Get or create API client (cached for performance)"""
    return ProcurementAPIClient()

# Check if API is available
def is_api_available() -> bool:
    """Check if the API is reachable"""
    client = get_api_client()
    health = client.health_check()
    return health.get("status") == "healthy"
