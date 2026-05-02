"""
Utility functions for the Procurement Intelligence Dashboard
Contains helper functions for data validation, formatting, and common operations.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
import logging
import json
import os

logger = logging.getLogger(__name__)

def format_currency(amount: Union[float, int], currency: str = '$') -> str:
    """
    Format amount as currency string.
    
    Args:
        amount (Union[float, int]): Amount to format
        currency (str): Currency symbol
        
    Returns:
        str: Formatted currency string
    """
    if pd.isna(amount):
        return 'N/A'
    
    try:
        return f"{currency}{amount:,.2f}"
    except (ValueError, TypeError):
        return f"{currency}0.00"

def format_number(number: Union[float, int], decimal_places: int = 2) -> str:
    """
    Format number with thousands separator.
    
    Args:
        number (Union[float, int]): Number to format
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted number string
    """
    if pd.isna(number):
        return 'N/A'
    
    try:
        return f"{number:,.{decimal_places}f}"
    except (ValueError, TypeError):
        return '0'

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value (float): Original value
        new_value (float): New value
        
    Returns:
        float: Percentage change
    """
    if old_value == 0:
        return 0.0
    
    try:
        return ((new_value - old_value) / old_value) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0.0

def validate_date_column(df: pd.DataFrame, column_name: str) -> bool:
    """
    Validate if a column contains valid dates.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        column_name (str): Column name to check
        
    Returns:
        bool: True if column contains valid dates
    """
    if column_name not in df.columns:
        return False
    
    try:
        pd.to_datetime(df[column_name])
        return True
    except (ValueError, TypeError):
        return False

def clean_numeric_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Clean numeric columns by removing non-numeric characters and converting to float.
    
    Args:
        df (pd.DataFrame): DataFrame to clean
        columns (List[str]): List of column names to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    cleaned_df = df.copy()
    
    for col in columns:
        if col in cleaned_df.columns:
            # Remove currency symbols and commas
            cleaned_df[col] = cleaned_df[col].astype(str).str.replace(r'[$,]', '', regex=True)
            
            # Convert to numeric, replace errors with NaN
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
    
    return cleaned_df

def get_date_range(df: pd.DataFrame, date_column: str = 'Date') -> Dict[str, Any]:
    """
    Get date range information from DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to analyze
        date_column (str): Name of date column
        
    Returns:
        Dict[str, Any]: Date range information
    """
    if date_column not in df.columns:
        return {'error': f'Date column {date_column} not found'}
    
    try:
        dates = pd.to_datetime(df[date_column])
        return {
            'min_date': dates.min(),
            'max_date': dates.max(),
            'total_days': (dates.max() - dates.min()).days,
            'date_range_valid': True
        }
    except Exception as e:
        return {'error': str(e), 'date_range_valid': False}

def create_summary_statistics(df: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
    """
    Create summary statistics for numeric columns.
    
    Args:
        df (pd.DataFrame): DataFrame to analyze
        numeric_columns (List[str]): List of numeric column names
        
    Returns:
        Dict[str, Any]: Summary statistics
    """
    summary = {}
    
    for col in numeric_columns:
        if col in df.columns:
            try:
                series = pd.to_numeric(df[col], errors='coerce').dropna()
                if len(series) > 0:
                    summary[col] = {
                        'count': len(series),
                        'mean': series.mean(),
                        'median': series.median(),
                        'std': series.std(),
                        'min': series.min(),
                        'max': series.max(),
                        'q25': series.quantile(0.25),
                        'q75': series.quantile(0.75)
                    }
                else:
                    summary[col] = {'error': 'No valid numeric data'}
            except Exception as e:
                summary[col] = {'error': str(e)}
        else:
            summary[col] = {'error': 'Column not found'}
    
    return summary

def safe_divide(numerator: Union[float, int], denominator: Union[float, int], default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default value if division fails.
    
    Args:
        numerator (Union[float, int]): Numerator
        denominator (Union[float, int]): Denominator
        default (float): Default value if division fails
        
    Returns:
        float: Result of division or default value
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (ValueError, TypeError, ZeroDivisionError):
        return default

def categorize_by_percentile(series: pd.Series, categories: List[str] = None) -> pd.Series:
    """
    Categorize values based on percentiles.
    
    Args:
        series (pd.Series): Series to categorize
        categories (List[str]): Category names
        
    Returns:
        pd.Series: Categorized series
    """
    if categories is None:
        categories = ['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High']
    
    try:
        percentiles = np.linspace(0, 100, len(categories) + 1)
        bins = [series.quantile(p/100) for p in percentiles]
        
        return pd.cut(series, bins=bins, labels=categories, include_lowest=True)
    except Exception as e:
        logger.error(f"Error categorizing series: {str(e)}")
        return pd.Series(['Medium'] * len(series), index=series.index)

def export_to_json(data: Any, file_path: str, indent: int = 2) -> bool:
    """
    Export data to JSON file.
    
    Args:
        data (Any): Data to export
        file_path (str): Output file path
        indent (int): JSON indentation
        
    Returns:
        bool: True if export successful
    """
    try:
        # Convert pandas objects to JSON-serializable format
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')
        elif isinstance(data, pd.Series):
            data = data.to_dict()
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent, default=str)
        
        logger.info(f"Data exported to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error exporting to JSON: {str(e)}")
        return False

def load_config_file(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_path (str): Path to configuration file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        return {}

def create_performance_score(metrics: Dict[str, float], weights: Dict[str, float] = None) -> float:
    """
    Create weighted performance score from metrics.
    
    Args:
        metrics (Dict[str, float]): Dictionary of metric values
        weights (Dict[str, float]): Dictionary of weights for each metric
        
    Returns:
        float: Weighted performance score
    """
    if weights is None:
        # Default equal weights
        weights = {key: 1.0 for key in metrics.keys()}
    
    try:
        weighted_sum = sum(metrics.get(key, 0) * weights.get(key, 0) for key in metrics.keys())
        total_weight = sum(weights.get(key, 0) for key in metrics.keys())
        
        if total_weight == 0:
            return 0.0
        
        return weighted_sum / total_weight
    except Exception as e:
        logger.error(f"Error calculating performance score: {str(e)}")
        return 0.0

def normalize_series(series: pd.Series, method: str = 'minmax') -> pd.Series:
    """
    Normalize a pandas series using specified method.
    
    Args:
        series (pd.Series): Series to normalize
        method (str): Normalization method ('minmax', 'zscore', 'robust')
        
    Returns:
        pd.Series: Normalized series
    """
    try:
        if method == 'minmax':
            return (series - series.min()) / (series.max() - series.min())
        elif method == 'zscore':
            return (series - series.mean()) / series.std()
        elif method == 'robust':
            median = series.median()
            mad = (series - median).abs().median()
            return (series - median) / mad
        else:
            logger.warning(f"Unknown normalization method: {method}")
            return series
    except Exception as e:
        logger.error(f"Error normalizing series: {str(e)}")
        return series

def detect_outliers(series: pd.Series, method: str = 'iqr', threshold: float = 1.5) -> pd.Series:
    """
    Detect outliers in a pandas series.
    
    Args:
        series (pd.Series): Series to analyze
        method (str): Detection method ('iqr', 'zscore')
        threshold (float): Threshold for outlier detection
        
    Returns:
        pd.Series: Boolean series indicating outliers
    """
    try:
        if method == 'iqr':
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            return (series < lower_bound) | (series > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((series - series.mean()) / series.std())
            return z_scores > threshold
        
        else:
            logger.warning(f"Unknown outlier detection method: {method}")
            return pd.Series([False] * len(series), index=series.index)
    
    except Exception as e:
        logger.error(f"Error detecting outliers: {str(e)}")
        return pd.Series([False] * len(series), index=series.index)

def create_time_periods(dates: pd.Series, frequency: str = 'M') -> pd.Series:
    """
    Create time periods from date series.
    
    Args:
        dates (pd.Series): Series of dates
        frequency (str): Frequency string ('D', 'W', 'M', 'Q', 'Y')
        
    Returns:
        pd.Series: Series of time periods
    """
    try:
        dates = pd.to_datetime(dates)
        return dates.dt.to_period(frequency)
    except Exception as e:
        logger.error(f"Error creating time periods: {str(e)}")
        return dates

def calculate_growth_rate(series: pd.Series, periods: int = 1) -> pd.Series:
    """
    Calculate growth rate for a time series.
    
    Args:
        series (pd.Series): Time series data
        periods (int): Number of periods to compare
        
    Returns:
        pd.Series: Growth rate series
    """
    try:
        return series.pct_change(periods=periods) * 100
    except Exception as e:
        logger.error(f"Error calculating growth rate: {str(e)}")
        return pd.Series([0.0] * len(series), index=series.index)

def filter_data_by_date_range(df: pd.DataFrame, date_column: str, 
                              start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Filter DataFrame by date range.
    
    Args:
        df (pd.DataFrame): DataFrame to filter
        date_column (str): Name of date column
        start_date (datetime): Start date
        end_date (datetime): End date
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    try:
        df[date_column] = pd.to_datetime(df[date_column])
        mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
        return df[mask]
    except Exception as e:
        logger.error(f"Error filtering by date range: {str(e)}")
        return df

def get_top_n_by_column(df: pd.DataFrame, column: str, n: int = 10, 
                       ascending: bool = False) -> pd.DataFrame:
    """
    Get top N rows by column value.
    
    Args:
        df (pd.DataFrame): DataFrame to analyze
        column (str): Column to sort by
        n (int): Number of top rows to return
        ascending (bool): Sort order
        
    Returns:
        pd.DataFrame: Top N rows
    """
    try:
        return df.nlargest(n, column) if not ascending else df.nsmallest(n, column)
    except Exception as e:
        logger.error(f"Error getting top N rows: {str(e)}")
        return df.head(n)

# Color schemes for visualizations
COLOR_SCHEMES = {
    'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
    'business': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#5C7CFA',
                 '#495057', '#F59F00', '#12B886', '#E64980', '#228BE6'],
    'green': ['#2E7D32', '#43A047', '#66BB6A', '#81C784', '#A5D6A7',
              '#C8E6C9', '#E8F5E8', '#F1F8E9', '#DCEDC8', '#C5E1A5'],
    'blue': ['#0D47A1', '#1565C0', '#1976D2', '#1E88E5', '#2196F3',
             '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB', '#E3F2FD']
}

def get_color_scheme(scheme_name: str = 'default') -> List[str]:
    """
    Get color scheme by name.
    
    Args:
        scheme_name (str): Name of color scheme
        
    Returns:
        List[str]: List of color hex codes
    """
    return COLOR_SCHEMES.get(scheme_name, COLOR_SCHEMES['default'])

# Configuration constants
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_CURRENCY = '$'
DEFAULT_DECIMAL_PLACES = 2

# Logging configuration
def setup_logging(level: str = 'INFO', log_file: str = None) -> None:
    """
    Setup logging configuration.
    
    Args:
        level (str): Logging level
        log_file (str): Optional log file path
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=handlers
    )

# Data validation schemas
REQUIRED_COLUMNS = {
    'basic': ['Date', 'Department', 'Supplier', 'Category', 'Amount'],
    'advanced': ['Date', 'Department', 'Supplier', 'Category', 'Amount', 'Status', 'Lead_Time'],
    'complete': ['Date', 'Delivery_Date', 'Department', 'Supplier', 'Category', 
                'Item_Description', 'Quantity', 'Unit_Price', 'Amount', 'Status', 
                'Priority', 'Lead_Time', 'Approved_By', 'Contract_ID']
}

def validate_data_schema(df: pd.DataFrame, schema_level: str = 'basic') -> Dict[str, Any]:
    """
    Validate DataFrame schema against required columns.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        schema_level (str): Schema level ('basic', 'advanced', 'complete')
        
    Returns:
        Dict[str, Any]: Validation results
    """
    required_cols = REQUIRED_COLUMNS.get(schema_level, REQUIRED_COLUMNS['basic'])
    missing_cols = set(required_cols) - set(df.columns)
    
    validation_result = {
        'is_valid': len(missing_cols) == 0,
        'missing_columns': list(missing_cols),
        'present_columns': list(df.columns),
        'required_columns': required_cols,
        'schema_level': schema_level
    }
    
    return validation_result
