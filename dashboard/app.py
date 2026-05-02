import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys

# Add src directory to path for custom modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.data_processor import ProcurementDataProcessor
from src.analytics import ProcurementAnalytics
from src.visualizations import ProcurementVisualizations

# Set page configuration
st.set_page_config(
    page_title="Procurement Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and process data
@st.cache_data
def load_data():
    try:
        # Try to load sample data from data directory
        processor = ProcurementDataProcessor()
        
        # Load sample data if available
        sample_data_path = '../data/sample_procurement_data.csv'
        if os.path.exists(sample_data_path):
            df = processor.load_data(sample_data_path, 'csv')
            # Convert date columns
            df['Date'] = pd.to_datetime(df['Date'])
            df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])
        else:
            # Generate sample data if file doesn't exist
            df = processor.generate_sample_data(num_records=2000)
            df = processor.clean_data()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        # Fallback to simple sample data
        return generate_simple_sample_data()

@st.cache_data
def generate_simple_sample_data():
    np.random.seed(42)
    date_range = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # Sample procurement data
    departments = ['IT', 'Operations', 'Marketing', 'Sales', 'HR', 'Finance', 'Legal']
    suppliers = [
        'TechCorp Solutions', 'OfficeSupply Co.', 'Marketing Pro', 'Cloud Services Inc.',
        'Hardware Hub', 'Software Systems', 'Consulting Group', 'Facility Management'
    ]
    categories = ['Hardware', 'Software', 'Services', 'Office Supplies', 'Marketing Materials', 'Consulting']
    
    data = []
    for date in date_range:
        for _ in range(np.random.randint(1, 5)):
            data.append({
                'Date': date,
                'Department': np.random.choice(departments),
                'Supplier': np.random.choice(suppliers),
                'Category': np.random.choice(categories),
                'Amount': np.random.uniform(100, 50000),
                'Status': np.random.choice(['Completed', 'Pending', 'Cancelled', 'On Hold'], p=[0.7, 0.2, 0.05, 0.05]),
                'Lead_Time': np.random.randint(1, 30)
            })
    
    return pd.DataFrame(data)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">📊 Procurement Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for filters
st.sidebar.header("📋 Filters & Controls")

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[datetime.now() - timedelta(days=30), datetime.now()],
    max_value=datetime.now()
)

# Department filter
department = st.sidebar.selectbox(
    "Department",
    ["All Departments", "IT", "Operations", "Marketing", "Sales", "HR"]
)

# Load data first to get dynamic supplier list
df = load_data()

# Get dynamic supplier list
suppliers = ["All Suppliers"] + sorted(df['Supplier'].unique().tolist())

# Supplier filter
supplier = st.sidebar.selectbox(
    "Supplier",
    suppliers
)

# Category filter
categories = ["All Categories"] + sorted(df['Category'].unique().tolist())
category = st.sidebar.selectbox(
    "Category",
    categories
)

# Status filter
status = st.sidebar.selectbox(
    "Order Status",
    ["All Statuses", "Completed", "Pending", "Cancelled", "On Hold"]
)

# Analytics section
st.sidebar.markdown("---")
st.sidebar.header("📊 Advanced Analytics")

if st.sidebar.button("Generate Insights"):
    with st.spinner("Analyzing data..."):
        try:
            analytics = ProcurementAnalytics(df)
            insights = analytics.generate_insights_report()
            st.session_state.insights = insights
            st.sidebar.success("Insights generated!")
        except Exception as e:
            st.sidebar.error(f"Error generating insights: {str(e)}")

# Apply filters
filtered_df = df.copy()

# Date range filter
if len(date_range) == 2:
    start_date, end_date = date_range
    # Convert to datetime64[ns] for proper comparison
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

# Department filter
if department != "All Departments":
    filtered_df = filtered_df[filtered_df['Department'] == department]

# Supplier filter
if supplier != "All Suppliers":
    filtered_df = filtered_df[filtered_df['Supplier'] == supplier]

# Category filter
if category != "All Categories":
    filtered_df = filtered_df[filtered_df['Category'] == category]

# Status filter
if status != "All Statuses":
    filtered_df = filtered_df[filtered_df['Status'] == status]

# Key Metrics Section
st.header("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_spend = filtered_df['Amount'].sum()
    spend_change = ((filtered_df['Amount'].sum() - df['Amount'].sum()) / df['Amount'].sum() * 100) if len(df) > 0 else 0
    st.metric("Total Spend", f"${total_spend:,.2f}", delta=f"{spend_change:.1f}%")

with col2:
    avg_order_value = filtered_df['Amount'].mean()
    st.metric("Avg Order Value", f"${avg_order_value:,.2f}")

with col3:
    total_orders = len(filtered_df)
    st.metric("Total Orders", f"{total_orders:,}")

with col4:
    avg_lead_time = filtered_df['Lead_Time'].mean()
    st.metric("Avg Lead Time", f"{avg_lead_time:.1f} days")

st.markdown("---")

# Charts Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Spend by Department")
    dept_spend = filtered_df.groupby('Department')['Amount'].sum().reset_index()
    fig_dept = px.pie(dept_spend, values='Amount', names='Department', 
                     title="Department-wise Spending")
    st.plotly_chart(fig_dept, use_container_width=True)

with col2:
    st.subheader("📈 Monthly Spending Trend")
    filtered_df['Month'] = pd.to_datetime(filtered_df['Date']).dt.to_period('M')
    monthly_spend = filtered_df.groupby('Month')['Amount'].sum().reset_index()
    monthly_spend['Month'] = monthly_spend['Month'].astype(str)
    
    fig_trend = px.line(monthly_spend, x='Month', y='Amount', 
                       title="Monthly Spending Trend",
                       markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

# Additional Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏢 Top Suppliers")
    supplier_spend = filtered_df.groupby('Supplier')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_supplier = px.bar(supplier_spend, x='Amount', y='Supplier',
                         orientation='h', title="Top 10 Suppliers by Spend")
    fig_supplier.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_supplier, use_container_width=True)

with col2:
    st.subheader("📦 Category Distribution")
    category_spend = filtered_df.groupby('Category')['Amount'].sum().reset_index()
    fig_category = px.sunburst(category_spend, path=['Category'], values='Amount',
                              title="Spending by Category")
    st.plotly_chart(fig_category, use_container_width=True)

# Data Table Section
st.header("📋 Recent Procurement Transactions")

# Sample recent transactions
recent_data = filtered_df.sort_values('Date', ascending=False).head(10)
st.dataframe(recent_data[['Date', 'Department', 'Supplier', 'Category', 'Amount', 'Status']], 
             use_container_width=True)

# Download button
csv = recent_data.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name='procurement_data_filtered.csv',
    mime='text/csv'
)

# Advanced Analytics Section
if 'insights' in st.session_state:
    st.markdown("---")
    st.header("🔍 Advanced Analytics Insights")
    
    insights = st.session_state.insights
    
    # Display insights in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Forecast", "🏆 Suppliers", "⚠️ Risks", "💡 Opportunities"])
    
    with tab1:
        st.subheader("Spending Forecast")
        forecast = insights['spending_forecast']
        
        # Create forecast chart
        forecast_df = pd.DataFrame({
            'Date': pd.to_datetime(forecast['dates']),
            'Forecast': forecast['values'],
            'Lower Bound': forecast['confidence_interval']['lower'],
            'Upper Bound': forecast['confidence_interval']['upper']
        })
        
        fig_forecast = go.Figure()
        
        # Historical data
        historical_data = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
        historical_data.index = historical_data.index.to_timestamp()
        
        fig_forecast.add_trace(go.Scatter(
            x=historical_data.index,
            y=historical_data.values,
            mode='lines+markers',
            name='Historical',
            line=dict(color='blue', width=3)
        ))
        
        # Forecast
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['Date'],
            y=forecast_df['Forecast'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='orange', width=3, dash='dash')
        ))
        
        # Confidence interval
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['Date'].tolist() + forecast_df['Date'][::-1].tolist(),
            y=forecast_df['Upper Bound'].tolist() + forecast_df['Lower Bound'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(255, 127, 14, 0.2)',
            line=dict(color='rgba(255, 127, 14, 0)'),
            name='Confidence Interval'
        ))
        
        fig_forecast.update_layout(
            title='Spending Forecast with Confidence Intervals',
            xaxis_title='Date',
            yaxis_title='Amount ($)',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Forecast metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model R²", f"{forecast['model_performance']['r_squared']:.3f}")
        with col2:
            st.metric("Next Month Forecast", f"${forecast['values'][0]:,.2f}")
        with col3:
            st.metric("Forecast Method", forecast['method'])
    
    with tab2:
        st.subheader("Supplier Performance Analysis")
        supplier_perf = insights['supplier_performance']
        
        # Top performers
        st.write("**🏆 Top Performing Suppliers:**")
        for supplier in supplier_perf['top_performers']:
            st.write(f"• {supplier}")
        
        # Suppliers needing attention
        if supplier_perf['needs_attention']:
            st.write("**⚠️ Suppliers Needing Attention:**")
            for supplier in supplier_perf['needs_attention']:
                st.write(f"• {supplier}")
        
        # Supplier metrics table
        supplier_metrics = supplier_perf['supplier_metrics'].reset_index()
        st.dataframe(supplier_metrics.head(10), use_container_width=True)
    
    with tab3:
        st.subheader("Risk Assessment")
        risk_assessment = insights['risk_assessment']
        
        # Overall risk level
        risk_color = {
            'Low': '🟢',
            'Medium': '🟡', 
            'High': '🔴'
        }
        
        st.write(f"**Overall Risk Level:** {risk_color.get(risk_assessment['risk_level'], '⚪')} {risk_assessment['risk_level']}")
        st.write(f"**Total Identified Risks:** {risk_assessment['total_risks']}")
        
        # High priority risks
        if risk_assessment['high_priority_risks']:
            st.write("**🚨 High Priority Risks:**")
            for risk in risk_assessment['high_priority_risks']:
                with st.expander(f"{risk['type']}: {risk['entity']}"):
                    st.write(f"**Description:** {risk['description']}")
                    st.write(f"**Mitigation:** {risk['mitigation']}")
        
        # All risks
        if risk_assessment['risks']:
            st.write("**📋 All Identified Risks:**")
            risks_df = pd.DataFrame(risk_assessment['risks'])
            st.dataframe(risks_df, use_container_width=True)
    
    with tab4:
        st.subheader("Optimization Opportunities")
        opportunities = insights['optimization_opportunities']
        
        st.write(f"**Total Opportunities:** {opportunities['total_opportunities']}")
        st.write(f"**Priority Areas:** {', '.join(opportunities['priority_areas'])}")
        
        if opportunities['opportunities']:
            for i, opp in enumerate(opportunities['opportunities'], 1):
                with st.expander(f"{i}. {opp['type']}"):
                    st.write(f"**Description:** {opp['description']}")
                    if 'potential_savings' in opp:
                        st.write(f"**Potential Savings:** {opp['potential_savings']}")
                    st.write(f"**Recommendation:** {opp.get('recommendation', 'Review and implement suggested actions')}")

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #666;">Procurement Intelligence Dashboard © 2024</div>', 
            unsafe_allow_html=True)
