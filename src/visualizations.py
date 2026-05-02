"""
Visualization Module for Procurement Intelligence Dashboard
Provides chart generation and data visualization utilities.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ProcurementVisualizations:
    """
    Visualization utilities for procurement data analysis.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize visualizations with processed data.
        
        Args:
            data (pd.DataFrame): Processed procurement data
        """
        self.data = data.copy()
        
    def create_spend_trend_chart(self, period: str = 'monthly') -> go.Figure:
        """
        Create spending trend visualization.
        
        Args:
            period (str): Time period ('daily', 'weekly', 'monthly', 'quarterly')
            
        Returns:
            go.Figure: Plotly figure
        """
        data = self.data.copy()
        
        # Group by specified period
        if period == 'daily':
            data['Period'] = data['Date'].dt.date
        elif period == 'weekly':
            data['Period'] = data['Date'].dt.to_period('W').dt.start_time
        elif period == 'monthly':
            data['Period'] = data['Date'].dt.to_period('M').dt.start_time
        elif period == 'quarterly':
            data['Period'] = data['Date'].dt.to_period('Q').dt.start_time
        else:
            data['Period'] = data['Date'].dt.to_period('M').dt.start_time
        
        spend_trend = data.groupby('Period')['Amount'].sum().reset_index()
        
        fig = go.Figure()
        
        # Add main trend line
        fig.add_trace(go.Scatter(
            x=spend_trend['Period'],
            y=spend_trend['Amount'],
            mode='lines+markers',
            name='Total Spend',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ))
        
        # Add moving average
        if len(spend_trend) > 3:
            window = min(3, len(spend_trend) // 2)
            spend_trend['MA'] = spend_trend['Amount'].rolling(window=window).mean()
            
            fig.add_trace(go.Scatter(
                x=spend_trend['Period'],
                y=spend_trend['MA'],
                mode='lines',
                name=f'{window}-Period Moving Average',
                line=dict(color='#ff7f0e', width=2, dash='dash')
            ))
        
        fig.update_layout(
            title=f'Spending Trend ({period.title()})',
            xaxis_title='Period',
            yaxis_title='Amount ($)',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_department_breakdown(self, chart_type: str = 'pie') -> go.Figure:
        """
        Create department spending breakdown visualization.
        
        Args:
            chart_type (str): Chart type ('pie', 'bar', 'treemap')
            
        Returns:
            go.Figure: Plotly figure
        """
        dept_spend = self.data.groupby('Department')['Amount'].sum().reset_index()
        dept_spend = dept_spend.sort_values('Amount', ascending=False)
        
        if chart_type == 'pie':
            fig = px.pie(
                dept_spend, 
                values='Amount', 
                names='Department',
                title='Spending by Department',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
        elif chart_type == 'bar':
            fig = px.bar(
                dept_spend,
                x='Department',
                y='Amount',
                title='Spending by Department',
                color='Amount',
                color_continuous_scale='Blues'
            )
            fig.update_xaxis(tickangle=45)
        elif chart_type == 'treemap':
            fig = px.treemap(
                dept_spend,
                path=['Department'],
                values='Amount',
                title='Spending by Department',
                color='Amount',
                color_continuous_scale='Blues'
            )
        else:
            fig = px.pie(dept_spend, values='Amount', names='Department', title='Spending by Department')
        
        fig.update_layout(template='plotly_white', height=400)
        return fig
    
    def create_supplier_analysis(self) -> go.Figure:
        """
        Create comprehensive supplier analysis visualization.
        
        Returns:
            go.Figure: Plotly figure with subplots
        """
        # Calculate supplier metrics
        supplier_metrics = self.data.groupby('Supplier').agg({
            'Amount': ['sum', 'count', 'mean'],
            'Lead_Time': 'mean',
            'Status': lambda x: (x == 'Completed').mean() * 100
        }).round(2)
        
        supplier_metrics.columns = ['Total_Spend', 'Order_Count', 'Avg_Order', 'Avg_Lead_Time', 'Completion_Rate']
        supplier_metrics = supplier_metrics.sort_values('Total_Spend', ascending=False).head(10)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Spend by Supplier', 'Order Count by Supplier', 
                          'Average Lead Time', 'Completion Rate'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Total Spend
        fig.add_trace(
            go.Bar(x=supplier_metrics.index, y=supplier_metrics['Total_Spend'],
                  name='Total Spend', marker_color='#1f77b4'),
            row=1, col=1
        )
        
        # Order Count
        fig.add_trace(
            go.Bar(x=supplier_metrics.index, y=supplier_metrics['Order_Count'],
                  name='Order Count', marker_color='#ff7f0e'),
            row=1, col=2
        )
        
        # Average Lead Time
        fig.add_trace(
            go.Bar(x=supplier_metrics.index, y=supplier_metrics['Avg_Lead_Time'],
                  name='Avg Lead Time', marker_color='#2ca02c'),
            row=2, col=1
        )
        
        # Completion Rate
        fig.add_trace(
            go.Bar(x=supplier_metrics.index, y=supplier_metrics['Completion_Rate'],
                  name='Completion Rate', marker_color='#d62728'),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text='Supplier Performance Analysis',
            showlegend=False,
            template='plotly_white',
            height=600
        )
        
        # Update x-axis labels
        for i in range(1, 3):
            for j in range(1, 3):
                fig.update_xaxes(tickangle=45, row=i, col=j)
        
        return fig
    
    def create_category_distribution(self) -> go.Figure:
        """
        Create category spending distribution visualization.
        
        Returns:
            go.Figure: Plotly figure
        """
        category_spend = self.data.groupby('Category')['Amount'].sum().reset_index()
        category_spend = category_spend.sort_values('Amount', ascending=False)
        
        # Create sunburst chart
        fig = go.Figure(go.Sunburst(
            labels=category_spend['Category'],
            values=category_spend['Amount'],
            parents=[""] * len(category_spend),
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Spend: $%{value:,.2f}<br>Percentage: %{percentParent:.1%}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Spending Distribution by Category',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def create_lead_time_analysis(self) -> go.Figure:
        """
        Create lead time analysis visualization.
        
        Returns:
            go.Figure: Plotly figure
        """
        # Lead time distribution by category
        lead_time_data = self.data.groupby('Category')['Lead_Time'].agg(['mean', 'std', 'count']).reset_index()
        lead_time_data = lead_time_data.sort_values('mean', ascending=False)
        
        # Create box plot for actual distribution
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Average Lead Time by Category', 'Lead Time Distribution'),
            specs=[[{"type": "bar"}, {"type": "box"}]]
        )
        
        # Bar chart of average lead times
        fig.add_trace(
            go.Bar(x=lead_time_data['Category'], y=lead_time_data['mean'],
                  name='Avg Lead Time', marker_color='#1f77b4',
                  error_y=dict(type='data', array=lead_time_data['std'])),
            row=1, col=1
        )
        
        # Box plot of lead time distribution
        for category in self.data['Category'].unique():
            category_data = self.data[self.data['Category'] == category]['Lead_Time']
            fig.add_trace(
                go.Box(y=category_data, name=category, boxpoints='outliers'),
                row=1, col=2
            )
        
        fig.update_layout(
            title_text='Lead Time Analysis',
            showlegend=False,
            template='plotly_white',
            height=500
        )
        
        fig.update_xaxes(tickangle=45, row=1, col=1)
        
        return fig
    
    def create_forecast_chart(self, forecast_data: Dict) -> go.Figure:
        """
        Create spending forecast visualization.
        
        Args:
            forecast_data (Dict): Forecast data from analytics module
            
        Returns:
            go.Figure: Plotly figure
        """
        # Get historical data
        historical_data = self.data.groupby(self.data['Date'].dt.to_period('M'))['Amount'].sum()
        historical_data.index = historical_data.index.to_timestamp()
        
        fig = go.Figure()
        
        # Add historical data
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=historical_data.values,
            mode='lines+markers',
            name='Historical',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ))
        
        # Add forecast
        forecast_dates = pd.to_datetime(forecast_data['dates'])
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=forecast_data['values'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=6)
        ))
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_dates.tolist() + forecast_dates[::-1].tolist(),
            y=forecast_data['confidence_interval']['upper'] + 
              forecast_data['confidence_interval']['lower'][::-1],
            fill='toself',
            fillcolor='rgba(255, 127, 14, 0.2)',
            line=dict(color='rgba(255, 127, 14, 0)'),
            name='Confidence Interval',
            hoverinfo="skip"
        ))
        
        fig.update_layout(
            title='Spending Forecast',
            xaxis_title='Date',
            yaxis_title='Amount ($)',
            hovermode='x unified',
            template='plotly_white',
            height=400,
            legend=dict(x=0, y=1)
        )
        
        return fig
    
    def create_risk_heatmap(self, risk_data: Dict) -> go.Figure:
        """
        Create risk assessment heatmap.
        
        Args:
            risk_data (Dict): Risk assessment data
            
        Returns:
            go.Figure: Plotly figure
        """
        risks = risk_data['risks']
        
        # Prepare data for heatmap
        risk_types = list(set(risk['type'] for risk in risks))
        entities = list(set(risk['entity'] for risk in risks))
        
        # Create risk matrix
        risk_matrix = pd.DataFrame(index=entities, columns=risk_types)
        
        for risk in risks:
            risk_score = {'High': 3, 'Medium': 2, 'Low': 1}[risk['risk_level']]
            risk_matrix.loc[risk['entity'], risk['type']] = risk_score
        
        risk_matrix = risk_matrix.fillna(0)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=risk_matrix.values,
            x=risk_matrix.columns,
            y=risk_matrix.index,
            colorscale='Reds',
            showscale=True,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>Risk Type: %{x}<br>Risk Level: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Risk Assessment Heatmap',
            xaxis_title='Risk Type',
            yaxis_title='Entity',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def create_kpi_dashboard(self, metrics: Dict) -> go.Figure:
        """
        Create KPI dashboard visualization.
        
        Args:
            metrics (Dict): Key performance indicators
            
        Returns:
            go.Figure: Plotly figure with gauge charts
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Completion Rate', 'Avg Lead Time', 'Cost Efficiency', 'Supplier Diversity'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        # Completion Rate Gauge
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=metrics.get('completion_rate', 0),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Completion Rate (%)"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=1, col=1
        )
        
        # Average Lead Time Gauge
        avg_lead_time = metrics.get('avg_lead_time', 0)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=avg_lead_time,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Avg Lead Time (Days)"},
                gauge={
                    'axis': {'range': [None, max(30, avg_lead_time * 1.5)]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 10], 'color': "lightgreen"},
                        {'range': [10, 20], 'color': "yellow"},
                        {'range': [20, 30], 'color': "lightcoral"}
                    ]
                }
            ),
            row=1, col=2
        )
        
        # Cost Efficiency (simplified metric)
        cost_efficiency = min(100, (metrics.get('total_orders', 1) / max(metrics.get('total_spend', 1), 1)) * 1000)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=cost_efficiency,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Cost Efficiency"},
                gauge={'axis': {'range': [None, 100]}}
            ),
            row=2, col=1
        )
        
        # Supplier Diversity
        supplier_diversity = metrics.get('total_suppliers', 1)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=supplier_diversity,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Supplier Count"},
                gauge={'axis': {'range': [None, max(20, supplier_diversity * 1.5)]}}
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text='KPI Dashboard',
            template='plotly_white',
            height=600
        )
        
        return fig
    
    def create_correlation_matrix(self) -> go.Figure:
        """
        Create correlation matrix for numeric variables.
        
        Returns:
            go.Figure: Plotly figure
        """
        # Select numeric columns
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.data[numeric_cols].corr()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.round(2).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            hovertemplate='<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Correlation Matrix',
            template='plotly_white',
            height=500,
            width=600
        )
        
        return fig
