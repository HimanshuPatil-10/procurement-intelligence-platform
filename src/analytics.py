"""
Analytics Module for Procurement Intelligence Dashboard
Provides advanced analytics and insights for procurement data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)

class ProcurementAnalytics:
    """
    Advanced analytics engine for procurement data.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize analytics with processed data.
        
        Args:
            data (pd.DataFrame): Processed procurement data
        """
        self.data = data.copy()
        self.insights = {}
        
    def spend_forecast(self, periods: int = 12) -> Dict:
        """
        Forecast future spending using simple moving average and trend analysis.
        
        Args:
            periods (int): Number of periods to forecast
            
        Returns:
            Dict: Forecast results with confidence intervals
        """
        # Prepare time series data
        monthly_data = self.data.groupby(self.data['Date'].dt.to_period('M'))['Amount'].sum()
        monthly_data.index = monthly_data.index.to_timestamp()
        
        # Simple moving average forecast
        window = min(3, len(monthly_data) // 2)
        if window < 1:
            window = 1
            
        ma_forecast = monthly_data.rolling(window=window).mean().iloc[-1]
        
        # Calculate trend
        x = np.arange(len(monthly_data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, monthly_data.values)
        
        # Generate forecast
        last_date = monthly_data.index[-1]
        if hasattr(last_date, 'to_timestamp'):
            last_date = last_date.to_timestamp()
        else:
            last_date = pd.Timestamp(last_date)
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=30), periods=periods, freq='ME')
        forecast_values = []
        
        for i in range(periods):
            trend_value = slope * (len(monthly_data) + i) + intercept
            # Combine MA and trend with weights
            forecast_value = 0.7 * ma_forecast + 0.3 * trend_value
            forecast_values.append(max(0, forecast_value))  # Ensure non-negative
        
        # Calculate confidence intervals (simplified)
        residuals = monthly_data.values - (slope * x + intercept)
        std_residual = np.std(residuals)
        
        forecast = {
            'dates': forecast_dates.tolist(),
            'values': forecast_values,
            'method': 'Moving Average + Linear Trend',
            'confidence_interval': {
                'lower': [max(0, v - 1.96 * std_residual) for v in forecast_values],
                'upper': [v + 1.96 * std_residual for v in forecast_values]
            },
            'model_performance': {
                'r_squared': r_value ** 2,
                'p_value': p_value
            }
        }
        
        return forecast
    
    def supplier_performance_analysis(self) -> Dict:
        """
        Analyze supplier performance across multiple dimensions.
        
        Returns:
            Dict: Supplier performance metrics and rankings
        """
        supplier_metrics = self.data.groupby('Supplier').agg({
            'Amount': ['sum', 'mean', 'count', 'std'],
            'Lead_Time': ['mean', 'std'],
            'Status': lambda x: (x == 'Completed').mean() * 100
        }).round(2)
        
        supplier_metrics.columns = [
            'Total_Spend', 'Avg_Order_Value', 'Order_Count', 'Spend_Volatility',
            'Avg_Lead_Time', 'Lead_Time_Volatility', 'Completion_Rate'
        ]
        
        # Calculate performance scores
        # Normalize metrics to 0-100 scale
        scaler = StandardScaler()
        
        # Higher is better: Completion_Rate, Total_Spend (weighted by importance)
        # Lower is better: Avg_Lead_Time, Spend_Volatility
        
        performance_data = supplier_metrics.copy()
        
        # Create composite score
        performance_data['Spend_Score'] = (performance_data['Total_Spend'] / performance_data['Total_Spend'].max()) * 100
        performance_data['Reliability_Score'] = performance_data['Completion_Rate']
        performance_data['Speed_Score'] = 100 - ((performance_data['Avg_Lead_Time'] - performance_data['Avg_Lead_Time'].min()) / 
                                                (performance_data['Avg_Lead_Time'].max() - performance_data['Avg_Lead_Time'].min()) * 100)
        performance_data['Consistency_Score'] = 100 - ((performance_data['Spend_Volatility'] - performance_data['Spend_Volatility'].min()) / 
                                                      (performance_data['Spend_Volatility'].max() - performance_data['Spend_Volatility'].min()) * 100)
        
        # Weighted composite score
        performance_data['Composite_Score'] = (
            0.3 * performance_data['Spend_Score'] +
            0.3 * performance_data['Reliability_Score'] +
            0.2 * performance_data['Speed_Score'] +
            0.2 * performance_data['Consistency_Score']
        )
        
        # Rank suppliers
        performance_data = performance_data.sort_values('Composite_Score', ascending=False)
        performance_data['Rank'] = range(1, len(performance_data) + 1)
        
        return {
            'supplier_metrics': performance_data,
            'top_performers': performance_data.head(5).index.tolist(),
            'needs_attention': performance_data.tail(3).index.tolist()
        }
    
    def category_analysis(self) -> Dict:
        """
        Analyze spending patterns and trends by category.
        
        Returns:
            Dict: Category analysis with insights
        """
        category_metrics = self.data.groupby('Category').agg({
            'Amount': ['sum', 'mean', 'count'],
            'Lead_Time': 'mean',
            'Quantity': 'sum'
        }).round(2)
        
        category_metrics.columns = ['Total_Spend', 'Avg_Order_Value', 'Order_Count', 'Avg_Lead_Time', 'Total_Quantity']
        
        # Calculate category growth rates
        monthly_category = self.data.groupby([
            self.data['Date'].dt.to_period('M'), 'Category'
        ])['Amount'].sum().unstack(fill_value=0)
        
        growth_rates = {}
        for category in monthly_category.columns:
            if len(monthly_category[category]) > 1:
                recent_avg = monthly_category[category].tail(3).mean()
                historical_avg = monthly_category[category].head(3).mean()
                if historical_avg > 0:
                    growth_rate = ((recent_avg - historical_avg) / historical_avg) * 100
                    growth_rates[category] = growth_rate
                else:
                    growth_rates[category] = 0
            else:
                growth_rates[category] = 0
        
        category_metrics['Growth_Rate'] = category_metrics.index.map(growth_rates)
        
        # Identify opportunities and risks
        opportunities = category_metrics[
            (category_metrics['Growth_Rate'] > 10) & 
            (category_metrics['Total_Spend'] > category_metrics['Total_Spend'].median())
        ].index.tolist()
        
        risks = category_metrics[
            (category_metrics['Growth_Rate'] < -10) & 
            (category_metrics['Order_Count'] > 5)
        ].index.tolist()
        
        return {
            'category_metrics': category_metrics.sort_values('Total_Spend', ascending=False),
            'growth_rates': growth_rates,
            'opportunities': opportunities,
            'risks': risks,
            'dominant_categories': category_metrics.head(3).index.tolist()
        }
    
    def cost_optimization_opportunities(self) -> Dict:
        """
        Identify cost optimization opportunities.
        
        Returns:
            Dict: Optimization recommendations
        """
        opportunities = []
        
        # 1. Analyze price variations for similar items
        if 'Item_Description' in self.data.columns:
            item_price_analysis = self.data.groupby('Item_Description').agg({
                'Unit_Price': ['mean', 'std', 'count'],
                'Amount': 'sum'
            }).round(2)
            
            item_price_analysis.columns = ['Avg_Price', 'Price_Volatility', 'Order_Count', 'Total_Spend']
            
            # Find items with high price volatility
            high_volatility_items = item_price_analysis[
                (item_price_analysis['Price_Volatility'] > item_price_analysis['Price_Volatility'].mean()) &
                (item_price_analysis['Order_Count'] > 3)
            ]
            
            if not high_volatility_items.empty:
                opportunities.append({
                    'type': 'Price Standardization',
                    'description': 'Standardize prices for items with high volatility',
                    'items': high_volatility_items.index.tolist(),
                    'potential_savings': high_volatility_items['Total_Spend'].sum() * 0.05  # Estimated 5% savings
                })
        
        # 2. Analyze supplier concentration risk
        supplier_concentration = self.data.groupby('Supplier')['Amount'].sum()
        top_supplier_share = supplier_concentration.iloc[0] / supplier_concentration.sum() if len(supplier_concentration) > 0 else 0
        
        if top_supplier_share > 0.4:  # More than 40% spend with one supplier
            opportunities.append({
                'type': 'Supplier Diversification',
                'description': f'Reduce dependency on top supplier ({top_supplier_share:.1%} of total spend)',
                'current_risk': top_supplier_share,
                'recommendation': 'Identify and qualify alternative suppliers'
            })
        
        # 3. Analyze order timing and batching opportunities
        if 'Date' in self.data.columns:
            daily_orders = self.data.groupby('Date').size()
            avg_daily_orders = daily_orders.mean()
            
            if avg_daily_orders < 2:  # Low order frequency
                opportunities.append({
                    'type': 'Order Batching',
                    'description': 'Consolidate small orders to reduce processing costs',
                    'current_avg_daily_orders': avg_daily_orders,
                    'potential_savings': 'Estimated 10-15% reduction in processing costs'
                })
        
        # 4. Analyze lead time optimization
        lead_time_analysis = self.data.groupby('Category')['Lead_Time'].agg(['mean', 'std'])
        long_lead_time_categories = lead_time_analysis[lead_time_analysis['mean'] > lead_time_analysis['mean'].mean()]
        
        if not long_lead_time_categories.empty:
            opportunities.append({
                'type': 'Lead Time Optimization',
                'description': 'Focus on categories with longer lead times',
                'categories': long_lead_time_categories.index.tolist(),
                'avg_lead_times': long_lead_time_categories['mean'].to_dict()
            })
        
        return {
            'opportunities': opportunities,
            'total_opportunities': len(opportunities),
            'priority_areas': [opp['type'] for opp in opportunities if opp['type'] in ['Price Standardization', 'Supplier Diversification']]
        }
    
    def risk_assessment(self) -> Dict:
        """
        Assess procurement risks across different dimensions.
        
        Returns:
            Dict: Risk assessment results
        """
        risks = []
        
        # 1. Supplier dependency risk
        supplier_spend = self.data.groupby('Supplier')['Amount'].sum()
        total_spend = supplier_spend.sum()
        
        for supplier, spend in supplier_spend.items():
            share = spend / total_spend
            if share > 0.3:  # More than 30% with single supplier
                risks.append({
                    'type': 'Supplier Dependency',
                    'entity': supplier,
                    'risk_level': 'High' if share > 0.5 else 'Medium',
                    'description': f'{share:.1%} of total spend with {supplier}',
                    'mitigation': 'Develop alternative suppliers'
                })
        
        # 2. Price volatility risk
        if 'Unit_Price' in self.data.columns:
            price_volatility = self.data.groupby('Category')['Unit_Price'].std()
            high_volatility = price_volatility[price_volatility > price_volatility.mean()]
            
            for category, volatility in high_volatility.items():
                risks.append({
                    'type': 'Price Volatility',
                    'entity': category,
                    'risk_level': 'Medium',
                    'description': f'High price volatility in {category}',
                    'mitigation': 'Consider long-term contracts or price locks'
                })
        
        # 3. Delivery delay risk
        lead_time_stats = self.data.groupby('Supplier')['Lead_Time'].agg(['mean', 'std'])
        delayed_suppliers = lead_time_stats[lead_time_stats['mean'] > lead_time_stats['mean'].mean() + lead_time_stats['std'].mean()]
        
        for supplier, stats in delayed_suppliers.iterrows():
            risks.append({
                'type': 'Delivery Delay',
                'entity': supplier,
                'risk_level': 'Medium',
                'description': f'Average lead time of {stats["mean"]:.1f} days for {supplier}',
                'mitigation': 'Review supplier performance and consider alternatives'
            })
        
        # 4. Spend concentration risk
        category_spend = self.data.groupby('Category')['Amount'].sum()
        top_category_share = category_spend.iloc[0] / category_spend.sum() if len(category_spend) > 0 else 0
        
        if top_category_share > 0.6:
            risks.append({
                'type': 'Spend Concentration',
                'entity': category_spend.index[0],
                'risk_level': 'High',
                'description': f'{top_category_share:.1%} of spend in single category',
                'mitigation': 'Diversify procurement categories'
            })
        
        # Calculate overall risk score
        risk_scores = {'High': 3, 'Medium': 2, 'Low': 1}
        overall_risk_score = sum(risk_scores[risk['risk_level']] for risk in risks) / max(len(risks), 1)
        
        return {
            'risks': risks,
            'total_risks': len(risks),
            'overall_risk_score': min(overall_risk_score, 3),  # Cap at 3
            'risk_level': 'High' if overall_risk_score > 2.5 else 'Medium' if overall_risk_score > 1.5 else 'Low',
            'high_priority_risks': [risk for risk in risks if risk['risk_level'] == 'High']
        }
    
    def generate_insights_report(self) -> Dict:
        """
        Generate comprehensive insights report.
        
        Returns:
            Dict: Complete insights report
        """
        self.insights = {
            'spending_forecast': self.spend_forecast(),
            'supplier_performance': self.supplier_performance_analysis(),
            'category_analysis': self.category_analysis(),
            'optimization_opportunities': self.cost_optimization_opportunities(),
            'risk_assessment': self.risk_assessment(),
            'generated_at': datetime.now().isoformat()
        }
        
        return self.insights
