"""
Pydantic Schemas for API Request/Response Validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal

# Procurement Order Schemas
class ProcurementOrderBase(BaseModel):
    order_id: str
    date: datetime
    delivery_date: Optional[datetime] = None
    department: str
    supplier: str
    category: str
    item_description: Optional[str] = None
    quantity: int
    unit_price: float
    amount: float
    status: str
    priority: Optional[str] = None
    lead_time: Optional[int] = None
    approved_by: Optional[str] = None
    contract_id: Optional[str] = None

class ProcurementOrderCreate(ProcurementOrderBase):
    pass

class ProcurementOrderResponse(ProcurementOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Supplier Schemas
class SupplierBase(BaseModel):
    supplier_id: str
    supplier_name: str
    category: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    contract_start_date: Optional[date] = None
    contract_end_date: Optional[date] = None
    payment_terms: Optional[str] = None
    rating: Optional[float] = None
    active: str = "Yes"

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Analytics Schemas
class MetricsResponse(BaseModel):
    total_spend: float
    total_orders: int
    avg_order_value: float
    median_order_value: float
    avg_lead_time: float
    total_suppliers: int
    total_departments: int
    total_categories: int
    completion_rate: float
    cancellation_rate: float
    avg_monthly_spend: Optional[float] = None
    peak_month: Optional[str] = None

class ForecastRequest(BaseModel):
    periods: int = Field(default=12, ge=1, le=24)
    confidence_level: float = Field(default=0.95, ge=0.8, le=0.99)

class ForecastResponse(BaseModel):
    method: str
    dates: List[str]
    values: List[float]
    confidence_interval: Dict[str, List[float]]
    model_performance: Dict[str, float]

class SupplierPerformance(BaseModel):
    supplier_metrics: List[Dict[str, Any]]
    top_performers: List[str]
    needs_attention: List[str]

class RiskAssessment(BaseModel):
    risk_level: str
    total_risks: int
    high_priority_risks: List[Dict[str, Any]]
    risks: List[Dict[str, Any]]

class OptimizationOpportunities(BaseModel):
    total_opportunities: int
    priority_areas: List[str]
    opportunities: List[Dict[str, Any]]

class InsightsResponse(BaseModel):
    spending_forecast: ForecastResponse
    supplier_performance: SupplierPerformance
    risk_assessment: RiskAssessment
    optimization_opportunities: OptimizationOpportunities

# Filter Schemas
class DataFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    department: Optional[str] = None
    supplier: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None

# Dashboard KPI Schema
class KPIDashboard(BaseModel):
    total_spend: float
    spend_change_percent: float
    avg_order_value: float
    total_orders: int
    avg_lead_time: float

# Health Check Schema
class HealthCheck(BaseModel):
    status: str
    version: str
    database_connected: bool
    timestamp: datetime
