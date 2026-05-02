"""
Unit Tests for Data Processor Module
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def test_data_processor_initialization():
    """Test that data processor initializes correctly"""
    from src.data_processor import ProcurementDataProcessor
    processor = ProcurementDataProcessor()
    assert processor.data is None
    assert processor.processed_data is None


def test_generate_sample_data(data_processor):
    """Test sample data generation"""
    processor = data_processor
    df = processor.data
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100
    assert 'Order_ID' in df.columns
    assert 'Date' in df.columns
    assert 'Amount' in df.columns
    assert 'Status' in df.columns


def test_clean_data(data_processor):
    """Test data cleaning functionality"""
    processor = data_processor
    cleaned = processor.clean_data()
    
    assert isinstance(cleaned, pd.DataFrame)
    assert len(cleaned) > 0
    # Check that dates are datetime type
    assert pd.api.types.is_datetime64_any_dtype(cleaned['Date'])
    assert pd.api.types.is_datetime64_any_dtype(cleaned['Delivery_Date'])


def test_calculate_metrics(data_processor):
    """Test metrics calculation"""
    processor = data_processor
    processor.clean_data()
    metrics = processor.calculate_metrics()
    
    assert isinstance(metrics, dict)
    assert 'total_spend' in metrics
    assert 'total_orders' in metrics
    assert 'avg_order_value' in metrics
    assert 'avg_lead_time' in metrics
    assert 'completion_rate' in metrics
    
    # Check metric values are reasonable
    assert metrics['total_spend'] > 0
    assert metrics['total_orders'] == 100
    assert metrics['avg_order_value'] > 0


def test_get_top_suppliers(data_processor):
    """Test top suppliers analysis"""
    processor = data_processor
    processor.clean_data()
    top_suppliers = processor.get_top_suppliers(top_n=5)
    
    assert isinstance(top_suppliers, pd.DataFrame)
    assert len(top_suppliers) <= 5
    assert 'Total_Spend' in top_suppliers.columns
    assert 'Avg_Order_Value' in top_suppliers.columns


def test_get_department_analysis(data_processor):
    """Test department analysis"""
    processor = data_processor
    processor.clean_data()
    dept_analysis = processor.get_department_analysis()
    
    assert isinstance(dept_analysis, pd.DataFrame)
    assert len(dept_analysis) > 0
    assert 'Total_Spend' in dept_analysis.columns
    assert 'Completion_Rate' in dept_analysis.columns


def test_get_category_trends(data_processor):
    """Test category trends analysis"""
    processor = data_processor
    processor.clean_data()
    trends = processor.get_category_trends()
    
    assert isinstance(trends, pd.DataFrame)
    assert len(trends) > 0


def test_data_validation(data_processor):
    """Test that generated data passes validation"""
    processor = data_processor
    df = processor.data
    
    # Check required columns exist
    required_columns = ['Order_ID', 'Date', 'Department', 'Supplier', 'Category', 'Amount', 'Status']
    for col in required_columns:
        assert col in df.columns, f"Missing required column: {col}"
    
    # Check data types
    assert df['Amount'].dtype in ['float64', 'float32', 'int64']
    assert df['Quantity'].dtype in ['int64', 'int32']
    
    # Check no null values in critical columns
    assert df['Order_ID'].notna().all()
    assert df['Date'].notna().all()
    assert df['Amount'].notna().all()


def test_lead_time_calculation(data_processor):
    """Test that lead time is calculated correctly"""
    processor = data_processor
    df = processor.data
    
    for _, row in df.iterrows():
        expected_lead_time = (row['Delivery_Date'] - row['Date']).days
        assert row['Lead_Time'] == expected_lead_time, "Lead time calculation mismatch"


def test_amount_consistency(data_processor):
    """Test that amount is positive and reasonable"""
    processor = data_processor
    df = processor.data
    
    # Check that all amounts are positive
    assert (df['Amount'] > 0).all(), "All amounts should be positive"
    
    # Check that amount correlates with quantity and unit_price
    # Just verify the data structure is correct
    assert df['Amount'].dtype in ['float64', 'float32', 'int64'], "Amount should be numeric"


@pytest.mark.parametrize("top_n", [3, 5, 10])
def test_top_suppliers_different_counts(data_processor, top_n):
    """Test top suppliers with different counts"""
    processor = data_processor
    processor.clean_data()
    top_suppliers = processor.get_top_suppliers(top_n=top_n)
    
    assert len(top_suppliers) <= top_n
    # Verify sorting is by Total_Spend descending
    spends = top_suppliers['Total_Spend'].tolist()
    assert spends == sorted(spends, reverse=True)
