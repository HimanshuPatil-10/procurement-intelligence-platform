"""
FastAPI Main Application - RESTful API for Procurement Intelligence Dashboard
"""

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processor import ProcurementDataProcessor
from src.analytics import ProcurementAnalytics
from api.models import get_db, init_db, ProcurementOrder, Supplier, DepartmentBudget
from api.schemas import (
    ProcurementOrderResponse, MetricsResponse, ForecastRequest, ForecastResponse,
    SupplierPerformance, RiskAssessment, OptimizationOpportunities, InsightsResponse,
    DataFilter, KPIDashboard, HealthCheck, SupplierResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="Procurement Intelligence API",
    description="RESTful API for procurement analytics and insights",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    # Load sample data if database is empty
    db = next(get_db())
    if db.query(ProcurementOrder).count() == 0:
        load_sample_data_to_db(db)

# Helper function to load sample data
def load_sample_data_to_db(db: Session):
    """Load sample procurement data into database"""
    try:
        processor = ProcurementDataProcessor()
        df = processor.generate_sample_data(num_records=500)
        
        for _, row in df.iterrows():
            order = ProcurementOrder(
                order_id=row['Order_ID'],
                date=pd.to_datetime(row['Date']),
                delivery_date=pd.to_datetime(row['Delivery_Date']),
                department=row['Department'],
                supplier=row['Supplier'],
                category=row['Category'],
                item_description=row['Item_Description'],
                quantity=int(row['Quantity']),
                unit_price=float(row['Unit_Price']),
                amount=float(row['Amount']),
                status=row['Status'],
                priority=row['Priority'],
                lead_time=int(row['Lead_Time']),
                approved_by=row['Approved_By'],
                contract_id=row['Contract_ID']
            )
            db.add(order)
        
        db.commit()
        print(f"Loaded {len(df)} sample records into database")
    except Exception as e:
        print(f"Error loading sample data: {e}")
        db.rollback()

# Health Check Endpoint
@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """Check API and database health"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_connected = True
    except:
        db_connected = False
    
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        database_connected=db_connected,
        timestamp=datetime.utcnow()
    )

# Get all procurement orders
@app.get("/orders", response_model=List[ProcurementOrderResponse], tags=["Data"])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department: Optional[str] = None,
    supplier: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get procurement orders with optional filtering"""
    query = db.query(ProcurementOrder)
    
    if department:
        query = query.filter(ProcurementOrder.department == department)
    if supplier:
        query = query.filter(ProcurementOrder.supplier == supplier)
    if status:
        query = query.filter(ProcurementOrder.status == status)
    
    orders = query.offset(skip).limit(limit).all()
    return orders

# Get distinct values for filters
@app.get("/filters/options", tags=["Data"])
async def get_filter_options(db: Session = Depends(get_db)):
    """Get distinct values for filter dropdowns"""
    departments = [d[0] for d in db.query(ProcurementOrder.department).distinct().all()]
    suppliers = [s[0] for s in db.query(ProcurementOrder.supplier).distinct().all()]
    categories = [c[0] for c in db.query(ProcurementOrder.category).distinct().all()]
    statuses = [s[0] for s in db.query(ProcurementOrder.status).distinct().all()]
    
    return {
        "departments": departments,
        "suppliers": suppliers,
        "categories": categories,
        "statuses": statuses
    }

# Get KPIs
@app.get("/kpis", response_model=KPIDashboard, tags=["Analytics"])
async def get_kpis(db: Session = Depends(get_db)):
    """Get key performance indicators"""
    try:
        # Convert SQL data to DataFrame for analytics
        orders = db.query(ProcurementOrder).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No data available")
        
        data = pd.DataFrame([{
            'Date': order.date,
            'Amount': order.amount,
            'Lead_Time': order.lead_time,
            'Department': order.department,
            'Supplier': order.supplier,
            'Category': order.category,
            'Status': order.status
        } for order in orders])
        
        processor = ProcurementDataProcessor()
        processor.data = data
        cleaned_data = processor.clean_data()
        metrics = processor.calculate_metrics()
        
        return KPIDashboard(
            total_spend=metrics['total_spend'],
            spend_change_percent=0.0,  # Calculate if historical data available
            avg_order_value=metrics['avg_order_value'],
            total_orders=metrics['total_orders'],
            avg_lead_time=metrics['avg_lead_time']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating KPIs: {str(e)}")

# Get metrics
@app.get("/metrics", response_model=MetricsResponse, tags=["Analytics"])
async def get_metrics(db: Session = Depends(get_db)):
    """Get comprehensive procurement metrics"""
    try:
        orders = db.query(ProcurementOrder).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No data available")
        
        data = pd.DataFrame([{
            'Date': order.date,
            'Amount': order.amount,
            'Lead_Time': order.lead_time,
            'Department': order.department,
            'Supplier': order.supplier,
            'Category': order.category,
            'Status': order.status
        } for order in orders])
        
        processor = ProcurementDataProcessor()
        processor.data = data
        cleaned_data = processor.clean_data()
        metrics = processor.calculate_metrics()
        
        return MetricsResponse(**metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating metrics: {str(e)}")

# Get spending forecast
@app.post("/analytics/forecast", response_model=ForecastResponse, tags=["Analytics"])
async def get_forecast(
    request: ForecastRequest,
    db: Session = Depends(get_db)
):
    """Get spending forecast with confidence intervals"""
    try:
        orders = db.query(ProcurementOrder).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No data available")
        
        data = pd.DataFrame([{
            'Date': order.date,
            'Amount': order.amount,
            'Lead_Time': order.lead_time,
            'Department': order.department,
            'Supplier': order.supplier,
            'Category': order.category,
            'Status': order.status
        } for order in orders])
        
        analytics = ProcurementAnalytics(data)
        forecast = analytics.spend_forecast(periods=request.periods)
        
        # Convert dates to strings for Pydantic validation
        dates_str = [str(d) for d in forecast['dates']]
        
        return ForecastResponse(
            method=forecast['method'],
            dates=dates_str,
            values=forecast['values'],
            confidence_interval=forecast['confidence_interval'],
            model_performance=forecast['model_performance']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")

# Get supplier performance
@app.get("/analytics/suppliers", response_model=SupplierPerformance, tags=["Analytics"])
async def get_supplier_performance(db: Session = Depends(get_db)):
    """Get supplier performance analysis"""
    try:
        orders = db.query(ProcurementOrder).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No data available")
        
        data = pd.DataFrame([{
            'Date': order.date,
            'Amount': order.amount,
            'Lead_Time': order.lead_time,
            'Department': order.department,
            'Supplier': order.supplier,
            'Category': order.category,
            'Status': order.status
        } for order in orders])
        
        analytics = ProcurementAnalytics(data)
        performance = analytics.supplier_performance_analysis()
        
        # Reset index to include Supplier as a column and convert to dict
        supplier_metrics_df = performance['supplier_metrics'].reset_index()
        
        return SupplierPerformance(
            supplier_metrics=supplier_metrics_df.to_dict('records'),
            top_performers=performance['top_performers'],
            needs_attention=performance['needs_attention']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing suppliers: {str(e)}")

# Get risk assessment
@app.get("/analytics/risks", response_model=RiskAssessment, tags=["Analytics"])
async def get_risk_assessment(db: Session = Depends(get_db)):
    """Get procurement risk assessment"""
    try:
        orders = db.query(ProcurementOrder).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No data available")
        
        data = pd.DataFrame([{
            'Date': order.date,
            'Amount': order.amount,
            'Lead_Time': order.lead_time,
            'Department': order.department,
            'Supplier': order.supplier,
            'Category': order.category,
            'Status': order.status
        } for order in orders])
        
        analytics = ProcurementAnalytics(data)
        risks = analytics.risk_assessment()
        
        return RiskAssessment(
            risk_level=risks['risk_level'],
            total_risks=risks['total_risks'],
            high_priority_risks=risks['high_priority_risks'],
            risks=risks['risks']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assessing risks: {str(e)}")

# Get optimization opportunities
@app.get("/analytics/opportunities", response_model=OptimizationOpportunities, tags=["Analytics"])
async def get_optimization_opportunities(db: Session = Depends(get_db)):
    """Get cost optimization opportunities"""
    try:
        orders = db.query(ProcurementOrder).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No data available")
        
        data = pd.DataFrame([{
            'Date': order.date,
            'Amount': order.amount,
            'Lead_Time': order.lead_time,
            'Department': order.department,
            'Supplier': order.supplier,
            'Category': order.category,
            'Status': order.status
        } for order in orders])
        
        analytics = ProcurementAnalytics(data)
        opportunities = analytics.cost_optimization_opportunities()
        
        return OptimizationOpportunities(
            total_opportunities=opportunities['total_opportunities'],
            priority_areas=opportunities['priority_areas'],
            opportunities=opportunities['opportunities']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding opportunities: {str(e)}")

# Get comprehensive insights
@app.get("/analytics/insights", response_model=InsightsResponse, tags=["Analytics"])
async def get_insights(db: Session = Depends(get_db)):
    """Get comprehensive insights report"""
    try:
        orders = db.query(ProcurementOrder).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No data available")
        
        data = pd.DataFrame([{
            'Date': order.date,
            'Amount': order.amount,
            'Lead_Time': order.lead_time,
            'Department': order.department,
            'Supplier': order.supplier,
            'Category': order.category,
            'Status': order.status
        } for order in orders])
        
        analytics = ProcurementAnalytics(data)
        insights = analytics.generate_insights_report()
        
        # Convert dates to strings for Pydantic validation
        forecast_dates_str = [str(d) for d in insights['spending_forecast']['dates']]
        
        # Reset index to include Supplier as a column and convert to dict
        supplier_metrics_df = insights['supplier_performance']['supplier_metrics'].reset_index()
        
        return InsightsResponse(
            spending_forecast=ForecastResponse(
                method=insights['spending_forecast']['method'],
                dates=forecast_dates_str,
                values=insights['spending_forecast']['values'],
                confidence_interval=insights['spending_forecast']['confidence_interval'],
                model_performance=insights['spending_forecast']['model_performance']
            ),
            supplier_performance=SupplierPerformance(
                supplier_metrics=supplier_metrics_df.to_dict('records'),
                top_performers=insights['supplier_performance']['top_performers'],
                needs_attention=insights['supplier_performance']['needs_attention']
            ),
            risk_assessment=RiskAssessment(
                risk_level=insights['risk_assessment']['risk_level'],
                total_risks=insights['risk_assessment']['total_risks'],
                high_priority_risks=insights['risk_assessment']['high_priority_risks'],
                risks=insights['risk_assessment']['risks']
            ),
            optimization_opportunities=OptimizationOpportunities(
                total_opportunities=insights['optimization_opportunities']['total_opportunities'],
                priority_areas=insights['optimization_opportunities']['priority_areas'],
                opportunities=insights['optimization_opportunities']['opportunities']
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Procurement Intelligence API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
