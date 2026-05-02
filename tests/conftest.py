"""
Pytest Configuration and Shared Fixtures
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models import Base, get_db
from api.main import app
from src.data_processor import ProcurementDataProcessor
from src.analytics import ProcurementAnalytics

# Use file-based SQLite for test database with session-scoped data
import tempfile

# Create test database file in project directory
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'test.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Populate test database with sample data once at session level
from api.models import ProcurementOrder

# Clear any existing data first (in case of previous test runs)
db = TestingSessionLocal()
db.query(ProcurementOrder).delete()
db.commit()
db.close()

# Generate and insert fresh test data
processor = ProcurementDataProcessor()
df = processor.generate_sample_data(num_records=100)

db = TestingSessionLocal()
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
db.close()

# Override dependency
@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture(scope="function")
def sample_procurement_data():
    """Generate sample procurement data for testing"""
    np.random.seed(42)
    
    data = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(100):
        order_date = base_date + timedelta(days=np.random.randint(0, 365))
        lead_time = np.random.randint(5, 45)
        delivery_date = order_date + timedelta(days=int(lead_time))
        
        data.append({
            'Order_ID': f'ORD-{i+1:06d}',
            'Date': order_date,
            'Delivery_Date': delivery_date,
            'Department': np.random.choice(['IT', 'Operations', 'Marketing', 'Sales', 'HR']),
            'Supplier': np.random.choice(['Supplier A', 'Supplier B', 'Supplier C']),
            'Category': np.random.choice(['Hardware', 'Software', 'Services']),
            'Item_Description': f'Test Item {i+1}',
            'Quantity': np.random.randint(1, 50),
            'Unit_Price': round(np.random.uniform(50, 500), 2),
            'Amount': round(np.random.uniform(1000, 25000), 2),
            'Status': np.random.choice(['Completed', 'Pending', 'Cancelled'], p=[0.7, 0.2, 0.1]),
            'Priority': np.random.choice(['High', 'Medium', 'Low'], p=[0.2, 0.6, 0.2]),
            'Lead_Time': int(lead_time),
            'Approved_By': np.random.choice(['John Doe', 'Jane Smith']),
            'Contract_ID': f'CONTRACT-{np.random.randint(1000, 9999)}'
        })
    
    return pd.DataFrame(data)

@pytest.fixture(scope="function")
def data_processor(sample_procurement_data):
    """Create a data processor with sample data"""
    processor = ProcurementDataProcessor()
    processor.data = sample_procurement_data
    return processor

@pytest.fixture(scope="function")
def analytics_engine(sample_procurement_data):
    """Create an analytics engine with sample data"""
    return ProcurementAnalytics(sample_procurement_data)
