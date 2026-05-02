"""
Data Processing Module for Procurement Intelligence Dashboard
Handles data loading, cleaning, and transformation operations.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcurementDataProcessor:
    """
    A comprehensive data processor for procurement data analysis.
    """
    
    def __init__(self):
        self.data = None
        self.processed_data = None
        
    def load_data(self, file_path: str, file_type: str = 'csv') -> pd.DataFrame:
        """
        Load data from various file formats.
        
        Args:
            file_path (str): Path to the data file
            file_type (str): Type of file ('csv', 'excel', 'json')
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            if file_type.lower() == 'csv':
                self.data = pd.read_csv(file_path)
            elif file_type.lower() == 'excel':
                self.data = pd.read_excel(file_path)
            elif file_type.lower() == 'json':
                self.data = pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
            logger.info(f"Successfully loaded {len(self.data)} records from {file_path}")
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def generate_sample_data(self, num_records: int = 1000) -> pd.DataFrame:
        """
        Generate sample procurement data for testing and demonstration.
        
        Args:
            num_records (int): Number of records to generate
            
        Returns:
            pd.DataFrame: Generated sample data
        """
        np.random.seed(42)
        
        # Define categories and options
        departments = ['IT', 'Operations', 'Marketing', 'Sales', 'HR', 'Finance', 'Legal']
        suppliers = [
            'TechCorp Solutions', 'OfficeSupply Co.', 'Marketing Pro', 'Cloud Services Inc.',
            'Hardware Hub', 'Software Systems', 'Consulting Group', 'Facility Management'
        ]
        categories = ['Hardware', 'Software', 'Services', 'Office Supplies', 'Marketing Materials', 'Consulting']
        statuses = ['Completed', 'Pending', 'Cancelled', 'On Hold']
        priorities = ['High', 'Medium', 'Low']
        
        # Generate date range
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate data
        data = []
        for i in range(num_records):
            order_date_idx = np.random.randint(0, len(date_range))
            order_date = date_range[order_date_idx]
            lead_time_days = int(np.random.randint(1, 60))
            delivery_date = order_date + pd.Timedelta(days=lead_time_days)
            
            data.append({
                'Order_ID': f'ORD-{i+1:06d}',
                'Date': order_date,
                'Delivery_Date': delivery_date,
                'Department': departments[np.random.randint(0, len(departments))],
                'Supplier': suppliers[np.random.randint(0, len(suppliers))],
                'Category': categories[np.random.randint(0, len(categories))],
                'Item_Description': f'Item {i+1}',
                'Quantity': int(np.random.randint(1, 100)),
                'Unit_Price': round(float(np.random.uniform(10, 1000)), 2),
                'Amount': round(float(np.random.uniform(100, 50000)), 2),
                'Status': statuses[np.random.randint(0, len(statuses))],
                'Priority': priorities[np.random.randint(0, len(priorities))],
                'Lead_Time': lead_time_days,
                'Approved_By': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams'][np.random.randint(0, 4)],
                'Contract_ID': f'CONTRACT-{int(np.random.randint(1000, 9999))}'
            })
        
        self.data = pd.DataFrame(data)
        logger.info(f"Generated {num_records} sample procurement records")
        return self.data
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the procurement data.
        
        Returns:
            pd.DataFrame: Cleaned data
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        cleaned_data = self.data.copy()
        
        # Convert date columns to datetime
        date_columns = ['Date', 'Delivery_Date']
        for col in date_columns:
            if col in cleaned_data.columns:
                cleaned_data[col] = pd.to_datetime(cleaned_data[col])
        
        # Handle missing values
        numeric_columns = cleaned_data.select_dtypes(include=[np.number]).columns
        cleaned_data[numeric_columns] = cleaned_data[numeric_columns].fillna(0)
        
        categorical_columns = cleaned_data.select_dtypes(include=['object']).columns
        cleaned_data[categorical_columns] = cleaned_data[categorical_columns].fillna('Unknown')
        
        # Remove duplicates
        initial_count = len(cleaned_data)
        cleaned_data = cleaned_data.drop_duplicates()
        removed_count = initial_count - len(cleaned_data)
        
        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate records")
        
        # Calculate total amount if not present
        if 'Quantity' in cleaned_data.columns and 'Unit_Price' in cleaned_data.columns and 'Amount' not in cleaned_data.columns:
            cleaned_data['Amount'] = cleaned_data['Quantity'] * cleaned_data['Unit_Price']
        
        self.processed_data = cleaned_data
        logger.info("Data cleaning completed successfully")
        return cleaned_data
    
    def calculate_metrics(self) -> Dict:
        """
        Calculate key procurement metrics.
        
        Returns:
            Dict: Dictionary containing calculated metrics
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Please clean data first.")
        
        data = self.processed_data
        
        metrics = {
            'total_spend': data['Amount'].sum(),
            'total_orders': len(data),
            'avg_order_value': data['Amount'].mean(),
            'median_order_value': data['Amount'].median(),
            'avg_lead_time': data['Lead_Time'].mean(),
            'total_suppliers': data['Supplier'].nunique(),
            'total_departments': data['Department'].nunique(),
            'total_categories': data['Category'].nunique(),
            'completion_rate': (data['Status'] == 'Completed').mean() * 100,
            'cancellation_rate': (data['Status'] == 'Cancelled').mean() * 100
        }
        
        # Add time-based metrics
        if 'Date' in data.columns:
            data['Month'] = data['Date'].dt.to_period('M')
            monthly_spend = data.groupby('Month')['Amount'].sum()
            metrics['avg_monthly_spend'] = monthly_spend.mean()
            metrics['peak_month'] = monthly_spend.idxmax().strftime('%Y-%m') if not monthly_spend.empty else None
        
        return metrics
    
    def get_top_suppliers(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get top suppliers by total spend.
        
        Args:
            top_n (int): Number of top suppliers to return
            
        Returns:
            pd.DataFrame: Top suppliers with their metrics
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Please clean data first.")
        
        supplier_metrics = self.processed_data.groupby('Supplier').agg({
            'Amount': ['sum', 'mean', 'count'],
            'Lead_Time': 'mean'
        }).round(2)
        
        supplier_metrics.columns = ['Total_Spend', 'Avg_Order_Value', 'Order_Count', 'Avg_Lead_Time']
        supplier_metrics = supplier_metrics.sort_values('Total_Spend', ascending=False).head(top_n)
        
        return supplier_metrics
    
    def get_department_analysis(self) -> pd.DataFrame:
        """
        Analyze spending by department.
        
        Returns:
            pd.DataFrame: Department-wise analysis
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Please clean data first.")
        
        dept_analysis = self.processed_data.groupby('Department').agg({
            'Amount': ['sum', 'mean', 'count'],
            'Lead_Time': 'mean',
            'Status': lambda x: (x == 'Completed').mean() * 100
        }).round(2)
        
        dept_analysis.columns = ['Total_Spend', 'Avg_Order_Value', 'Order_Count', 'Avg_Lead_Time', 'Completion_Rate']
        dept_analysis = dept_analysis.sort_values('Total_Spend', ascending=False)
        
        return dept_analysis
    
    def get_category_trends(self) -> pd.DataFrame:
        """
        Analyze spending trends by category over time.
        
        Returns:
            pd.DataFrame: Category-wise monthly trends
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Please clean data first.")
        
        data = self.processed_data.copy()
        data['Month'] = data['Date'].dt.to_period('M')
        
        category_trends = data.groupby(['Month', 'Category'])['Amount'].sum().unstack(fill_value=0)
        
        return category_trends
    
    def export_processed_data(self, file_path: str, file_type: str = 'csv') -> None:
        """
        Export processed data to file.
        
        Args:
            file_path (str): Output file path
            file_type (str): Output file type ('csv', 'excel', 'json')
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Please clean data first.")
        
        try:
            if file_type.lower() == 'csv':
                self.processed_data.to_csv(file_path, index=False)
            elif file_type.lower() == 'excel':
                self.processed_data.to_excel(file_path, index=False)
            elif file_type.lower() == 'json':
                self.processed_data.to_json(file_path, orient='records', date_format='iso')
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
            logger.info(f"Successfully exported processed data to {file_path}")
            
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            raise


# Utility functions
def load_configuration(config_path: str) -> Dict:
    """
    Load configuration from JSON file.
    
    Args:
        config_path (str): Path to configuration file
        
    Returns:
        Dict: Configuration dictionary
    """
    import json
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return {}


def validate_data_schema(data: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that data contains required columns.
    
    Args:
        data (pd.DataFrame): Data to validate
        required_columns (List[str]): List of required column names
        
    Returns:
        bool: True if all required columns are present
    """
    missing_columns = set(required_columns) - set(data.columns)
    if missing_columns:
        logger.warning(f"Missing required columns: {missing_columns}")
        return False
    return True
