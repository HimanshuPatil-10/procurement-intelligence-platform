"""
Integration Tests for FastAPI Endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "database_connected" in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data


def test_get_orders(client):
    """Test getting procurement orders"""
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Database should have sample data loaded
    assert len(data) > 0


def test_get_orders_with_pagination(client):
    """Test orders pagination"""
    response = client.get("/orders?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_orders_with_filters(client):
    """Test orders with department filter"""
    # First get available departments
    filter_response = client.get("/filters/options")
    assert filter_response.status_code == 200
    filters = filter_response.json()
    
    if filters["departments"]:
        dept = filters["departments"][0]
        response = client.get(f"/orders?department={dept}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


def test_get_filter_options(client):
    """Test filter options endpoint"""
    response = client.get("/filters/options")
    assert response.status_code == 200
    data = response.json()
    
    assert "departments" in data
    assert "suppliers" in data
    assert "categories" in data
    assert "statuses" in data
    
    assert isinstance(data["departments"], list)
    assert isinstance(data["suppliers"], list)


def test_get_kpis(client):
    """Test KPIs endpoint"""
    response = client.get("/kpis")
    assert response.status_code == 200
    data = response.json()
    
    assert "total_spend" in data
    assert "spend_change_percent" in data
    assert "avg_order_value" in data
    assert "total_orders" in data
    assert "avg_lead_time" in data


def test_get_metrics(client):
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    
    required_metrics = [
        "total_spend", "total_orders", "avg_order_value",
        "median_order_value", "avg_lead_time", "total_suppliers",
        "total_departments", "total_categories", "completion_rate",
        "cancellation_rate"
    ]
    
    for metric in required_metrics:
        assert metric in data, f"Missing metric: {metric}"


def test_get_forecast(client):
    """Test forecast endpoint"""
    request_data = {
        "periods": 6,
        "confidence_level": 0.95
    }
    response = client.post("/analytics/forecast", json=request_data)
    assert response.status_code == 200
    data = response.json()
    
    assert "method" in data
    assert "dates" in data
    assert "values" in data
    assert "confidence_interval" in data
    assert "model_performance" in data
    
    assert len(data["dates"]) == 6
    assert len(data["values"]) == 6


def test_get_supplier_performance(client):
    """Test supplier performance endpoint"""
    response = client.get("/analytics/suppliers")
    assert response.status_code == 200
    data = response.json()
    
    assert "supplier_metrics" in data
    assert "top_performers" in data
    assert "needs_attention" in data


def test_get_risk_assessment(client):
    """Test risk assessment endpoint"""
    response = client.get("/analytics/risks")
    assert response.status_code == 200
    data = response.json()
    
    assert "risk_level" in data
    assert "total_risks" in data
    assert "high_priority_risks" in data
    assert "risks" in data
    
    assert data["risk_level"] in ["Low", "Medium", "High"]


def test_get_optimization_opportunities(client):
    """Test optimization opportunities endpoint"""
    response = client.get("/analytics/opportunities")
    assert response.status_code == 200
    data = response.json()
    
    assert "total_opportunities" in data
    assert "priority_areas" in data
    assert "opportunities" in data


def test_get_insights(client):
    """Test comprehensive insights endpoint"""
    response = client.get("/analytics/insights")
    assert response.status_code == 200
    data = response.json()
    
    assert "spending_forecast" in data
    assert "supplier_performance" in data
    assert "risk_assessment" in data
    assert "optimization_opportunities" in data


def test_api_error_handling(client):
    """Test API error handling"""
    # Test with invalid forecast parameters
    response = client.post("/analytics/forecast", json={"periods": 50})
    # Should fail validation (max is 24)
    assert response.status_code == 422


def test_docs_accessible(client):
    """Test that API docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema(client):
    """Test OpenAPI schema generation"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
