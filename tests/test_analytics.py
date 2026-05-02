"""
Unit Tests for Analytics Module
"""

import pytest
import pandas as pd
import numpy as np


def test_analytics_initialization(analytics_engine):
    """Test analytics engine initialization"""
    analytics = analytics_engine
    assert isinstance(analytics.data, pd.DataFrame)
    assert len(analytics.data) == 100


def test_spend_forecast(analytics_engine):
    """Test spend forecasting"""
    analytics = analytics_engine
    forecast = analytics.spend_forecast(periods=12)
    
    assert isinstance(forecast, dict)
    assert 'method' in forecast
    assert 'dates' in forecast
    assert 'values' in forecast
    assert 'confidence_interval' in forecast
    assert 'model_performance' in forecast
    
    # Check forecast structure
    assert len(forecast['dates']) == 12
    assert len(forecast['values']) == 12
    assert len(forecast['confidence_interval']['lower']) == 12
    assert len(forecast['confidence_interval']['upper']) == 12
    
    # Check model performance metrics
    assert 'r_squared' in forecast['model_performance']
    assert 'p_value' in forecast['model_performance']


def test_supplier_performance_analysis(analytics_engine):
    """Test supplier performance analysis"""
    analytics = analytics_engine
    performance = analytics.supplier_performance_analysis()
    
    assert isinstance(performance, dict)
    assert 'supplier_metrics' in performance
    assert 'top_performers' in performance
    assert 'needs_attention' in performance
    
    # Check structure
    assert isinstance(performance['supplier_metrics'], pd.DataFrame)
    assert isinstance(performance['top_performers'], list)
    assert isinstance(performance['needs_attention'], list)


def test_risk_assessment(analytics_engine):
    """Test risk assessment"""
    analytics = analytics_engine
    risks = analytics.risk_assessment()
    
    assert isinstance(risks, dict)
    assert 'risk_level' in risks
    assert 'total_risks' in risks
    assert 'high_priority_risks' in risks
    assert 'risks' in risks
    
    # Validate risk level
    assert risks['risk_level'] in ['Low', 'Medium', 'High']
    assert isinstance(risks['total_risks'], int)
    assert risks['total_risks'] >= 0


def test_cost_optimization_opportunities(analytics_engine):
    """Test cost optimization analysis"""
    analytics = analytics_engine
    opportunities = analytics.cost_optimization_opportunities()
    
    assert isinstance(opportunities, dict)
    assert 'total_opportunities' in opportunities
    assert 'priority_areas' in opportunities
    assert 'opportunities' in opportunities
    
    assert isinstance(opportunities['total_opportunities'], int)
    assert isinstance(opportunities['priority_areas'], list)
    assert isinstance(opportunities['opportunities'], list)


def test_category_analysis(analytics_engine):
    """Test category analysis"""
    analytics = analytics_engine
    analysis = analytics.category_analysis()
    
    assert isinstance(analysis, dict)
    assert 'category_metrics' in analysis
    assert 'growth_rates' in analysis
    assert 'opportunities' in analysis
    assert 'risks' in analysis
    assert 'dominant_categories' in analysis
    
    # Check metrics
    assert isinstance(analysis['category_metrics'], pd.DataFrame)
    assert len(analysis['category_metrics']) > 0


def test_generate_insights_report(analytics_engine):
    """Test comprehensive insights report generation"""
    analytics = analytics_engine
    insights = analytics.generate_insights_report()
    
    assert isinstance(insights, dict)
    assert 'spending_forecast' in insights
    assert 'supplier_performance' in insights
    assert 'risk_assessment' in insights
    assert 'optimization_opportunities' in insights
    
    # Validate all components are present and properly structured
    assert isinstance(insights['spending_forecast'], dict)
    assert isinstance(insights['supplier_performance'], dict)
    assert isinstance(insights['risk_assessment'], dict)
    assert isinstance(insights['optimization_opportunities'], dict)


def test_forecast_values_non_negative(analytics_engine):
    """Test that forecast values are non-negative"""
    analytics = analytics_engine
    forecast = analytics.spend_forecast(periods=6)
    
    for value in forecast['values']:
        assert value >= 0, "Forecast value should be non-negative"


def test_confidence_intervals_valid(analytics_engine):
    """Test that confidence intervals are valid (upper > lower)"""
    analytics = analytics_engine
    forecast = analytics.spend_forecast(periods=6)
    
    lower_bounds = forecast['confidence_interval']['lower']
    upper_bounds = forecast['confidence_interval']['upper']
    
    for lower, upper in zip(lower_bounds, upper_bounds):
        assert upper >= lower, "Upper bound should be >= lower bound"


def test_r_squared_in_valid_range(analytics_engine):
    """Test that R-squared is in valid range [-1, 1]"""
    analytics = analytics_engine
    forecast = analytics.spend_forecast(periods=6)
    
    r_squared = forecast['model_performance']['r_squared']
    assert -1 <= r_squared <= 1, "R-squared should be in range [-1, 1]"


def test_supplier_metrics_has_required_columns(analytics_engine):
    """Test that supplier metrics has all required columns"""
    analytics = analytics_engine
    performance = analytics.supplier_performance_analysis()
    
    metrics_df = performance['supplier_metrics']
    required_columns = [
        'Total_Spend', 'Order_Count', 'Avg_Order_Value',
        'Avg_Lead_Time', 'Completion_Rate', 'Composite_Score',
        'Spend_Volatility', 'Lead_Time_Volatility'
    ]
    
    for col in required_columns:
        assert col in metrics_df.columns, f"Missing column: {col}"
