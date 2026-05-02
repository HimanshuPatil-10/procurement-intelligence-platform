"""
SQLAlchemy Database Models for Procurement Intelligence Dashboard
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class ProcurementOrder(Base):
    """Database model for procurement orders"""
    __tablename__ = "procurement_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    date = Column(DateTime, index=True)
    delivery_date = Column(DateTime)
    department = Column(String, index=True)
    supplier = Column(String, index=True)
    category = Column(String, index=True)
    item_description = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    amount = Column(Float)
    status = Column(String, index=True)
    priority = Column(String)
    lead_time = Column(Integer)
    approved_by = Column(String)
    contract_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Supplier(Base):
    """Database model for suppliers"""
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(String, unique=True, index=True)
    supplier_name = Column(String)
    category = Column(String)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    contract_start_date = Column(Date)
    contract_end_date = Column(Date)
    payment_terms = Column(String)
    rating = Column(Float)
    active = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class DepartmentBudget(Base):
    """Database model for department budgets"""
    __tablename__ = "department_budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)
    quarter = Column(String, index=True)
    budget = Column(Float)
    actual_spend = Column(Float)
    variance = Column(Float)
    variance_percentage = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./procurement_dashboard.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Database session generator"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
