"""
Configuration file for the Procurement Intelligence Dashboard
Contains settings, constants, and configuration parameters.
"""

import os
from typing import Dict, List, Any
from datetime import datetime

# Project Information
PROJECT_NAME = "Procurement Intelligence Dashboard"
VERSION = "1.0.0"
AUTHOR = "Procurement Intelligence Team"
DESCRIPTION = "Comprehensive procurement analytics and insights dashboard"

# File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
NOTEBOOKS_DIR = os.path.join(BASE_DIR, 'notebooks')
DASHBOARD_DIR = os.path.join(BASE_DIR, 'dashboard')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# Data File Paths
SAMPLE_DATA_FILE = os.path.join(DATA_DIR, 'sample_procurement_data.csv')
SUPPLIER_MASTER_FILE = os.path.join(DATA_DIR, 'supplier_master_data.csv')
BUDGET_DATA_FILE = os.path.join(DATA_DIR, 'department_budget.csv')

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'title': 'Procurement Intelligence Dashboard',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'page_icon': '📊',
    'theme': {
        'base': 'light',
        'primaryColor': '#1f77b4',
        'backgroundColor': '#ffffff',
        'secondaryBackgroundColor': '#f0f2f6',
        'textColor': '#262730'
    }
}

# Data Processing Configuration
DATA_CONFIG = {
    'default_date_format': '%Y-%m-%d',
    'default_currency': '$',
    'decimal_places': 2,
    'sample_data_size': 2000,
    'cache_ttl': 3600,  # Cache time-to-live in seconds
    'max_file_size_mb': 100,
    'supported_formats': ['csv', 'excel', 'json'],
    'encoding': 'utf-8'
}

# Analytics Configuration
ANALYTICS_CONFIG = {
    'forecast_periods': 12,
    'confidence_level': 0.95,
    'min_data_points': 10,
    'outlier_threshold': 1.5,
    'performance_weights': {
        'reliability': 0.3,
        'speed': 0.25,
        'volume': 0.25,
        'consistency': 0.2
    },
    'risk_thresholds': {
        'high': 0.7,
        'medium': 0.4,
        'low': 0.0
    }
}

# Visualization Configuration
VIZ_CONFIG = {
    'default_color_scheme': 'default',
    'chart_height': 400,
    'chart_width': None,  # Auto-adjust
    'show_grid': True,
    'show_legend': True,
    'hover_mode': 'x unified',
    'export_formats': ['png', 'svg', 'pdf'],
    'animation_duration': 1000
}

# KPI Configuration
KPI_CONFIG = {
    'metrics': [
        'total_spend',
        'avg_order_value', 
        'total_orders',
        'avg_lead_time'
    ],
    'targets': {
        'total_spend_growth': 10.0,  # Target growth percentage
        'avg_lead_time_target': 15.0,  # Target days
        'completion_rate_target': 95.0,  # Target percentage
        'cost_savings_target': 5.0  # Target savings percentage
    },
    'alert_thresholds': {
        'spending_increase': 20.0,  # Alert if spending increases by >20%
        'lead_time_increase': 30.0,  # Alert if lead time increases by >30%
        'completion_rate_drop': 10.0  # Alert if completion rate drops by >10%
    }
}

# Department Configuration
DEPARTMENTS = {
    'IT': {
        'name': 'Information Technology',
        'budget_category': 'Technology',
        'typical_categories': ['Hardware', 'Software', 'Services'],
        'spending_pattern': 'regular'
    },
    'Operations': {
        'name': 'Operations',
        'budget_category': 'Operations',
        'typical_categories': ['Services', 'Hardware', 'Office Supplies'],
        'spending_pattern': 'steady'
    },
    'Marketing': {
        'name': 'Marketing',
        'budget_category': 'Marketing',
        'typical_categories': ['Marketing Materials', 'Services'],
        'spending_pattern': 'seasonal'
    },
    'Sales': {
        'name': 'Sales',
        'budget_category': 'Sales',
        'typical_categories': ['Services', 'Hardware'],
        'spending_pattern': 'commission_based'
    },
    'HR': {
        'name': 'Human Resources',
        'budget_category': 'Administration',
        'typical_categories': ['Services', 'Office Supplies'],
        'spending_pattern': 'regular'
    },
    'Finance': {
        'name': 'Finance',
        'budget_category': 'Finance',
        'typical_categories': ['Software', 'Services'],
        'spending_pattern': 'steady'
    },
    'Legal': {
        'name': 'Legal',
        'budget_category': 'Legal',
        'typical_categories': ['Services', 'Software'],
        'spending_pattern': 'project_based'
    }
}

# Category Configuration
CATEGORIES = {
    'Hardware': {
        'name': 'Hardware & Equipment',
        'typical_lead_time': 14,
        'price_volatility': 'medium',
        'supplier_concentration': 'low'
    },
    'Software': {
        'name': 'Software & Licenses',
        'typical_lead_time': 7,
        'price_volatility': 'low',
        'supplier_concentration': 'medium'
    },
    'Services': {
        'name': 'Professional Services',
        'typical_lead_time': 21,
        'price_volatility': 'high',
        'supplier_concentration': 'low'
    },
    'Office Supplies': {
        'name': 'Office Supplies',
        'typical_lead_time': 5,
        'price_volatility': 'low',
        'supplier_concentration': 'medium'
    },
    'Marketing Materials': {
        'name': 'Marketing Materials',
        'typical_lead_time': 10,
        'price_volatility': 'medium',
        'supplier_concentration': 'low'
    },
    'Consulting': {
        'name': 'Consulting Services',
        'typical_lead_time': 30,
        'price_volatility': 'high',
        'supplier_concentration': 'low'
    }
}

# Status Configuration
ORDER_STATUSES = {
    'Completed': {
        'color': '#28a745',
        'icon': '✅',
        'description': 'Order successfully completed'
    },
    'Pending': {
        'color': '#ffc107',
        'icon': '⏳',
        'description': 'Order is pending processing'
    },
    'Cancelled': {
        'color': '#dc3545',
        'icon': '❌',
        'description': 'Order was cancelled'
    },
    'On Hold': {
        'color': '#6c757d',
        'icon': '⏸️',
        'description': 'Order is on hold'
    }
}

# Priority Configuration
PRIORITIES = {
    'High': {
        'color': '#dc3545',
        'weight': 3,
        'description': 'High priority - requires immediate attention'
    },
    'Medium': {
        'color': '#ffc107',
        'weight': 2,
        'description': 'Medium priority - normal processing'
    },
    'Low': {
        'color': '#28a745',
        'weight': 1,
        'description': 'Low priority - can be processed later'
    }
}

# Risk Configuration
RISK_TYPES = {
    'Supplier Dependency': {
        'severity': 'high',
        'mitigation': 'Develop alternative suppliers',
        'monitoring_frequency': 'monthly'
    },
    'Performance Risk': {
        'severity': 'medium',
        'mitigation': 'Implement performance improvement plans',
        'monitoring_frequency': 'weekly'
    },
    'Price Volatility': {
        'severity': 'medium',
        'mitigation': 'Consider long-term contracts',
        'monitoring_frequency': 'monthly'
    },
    'Delivery Delay': {
        'severity': 'medium',
        'mitigation': 'Review logistics and delivery processes',
        'monitoring_frequency': 'weekly'
    },
    'Spend Concentration': {
        'severity': 'high',
        'mitigation': 'Diversify procurement categories',
        'monitoring_frequency': 'quarterly'
    }
}

# Supplier Segmentation Configuration
SUPPLIER_SEGMENTS = {
    'Strategic': {
        'description': 'High spend, high performance suppliers',
        'management_approach': 'Partnership relationship',
        'review_frequency': 'quarterly'
    },
    'Critical': {
        'description': 'High spend, low performance suppliers',
        'management_approach': 'Performance improvement focus',
        'review_frequency': 'monthly'
    },
    'Preferred': {
        'description': 'Low spend, high performance suppliers',
        'management_approach': 'Maintain relationship',
        'review_frequency': 'semi-annually'
    },
    'Approved': {
        'description': 'Low spend, medium performance suppliers',
        'management_approach': 'Standard procurement',
        'review_frequency': 'annually'
    },
    'Development': {
        'description': 'Low spend, low performance suppliers',
        'management_approach': 'Develop or replace',
        'review_frequency': 'quarterly'
    }
}

# Email Configuration (for notifications)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'use_tls': True,
    'sender_email': os.getenv('EMAIL_SENDER', ''),
    'sender_password': os.getenv('EMAIL_PASSWORD', ''),
    'notification_recipients': os.getenv('EMAIL_RECIPIENTS', '').split(','),
    'templates': {
        'risk_alert': 'risk_alert_template.html',
        'opportunity_found': 'opportunity_template.html',
        'monthly_report': 'monthly_report_template.html'
    }
}

# API Configuration
API_CONFIG = {
    'base_url': os.getenv('API_BASE_URL', 'http://localhost:8000'),
    'timeout': 30,
    'retry_attempts': 3,
    'rate_limit': 100,  # requests per minute
    'authentication': {
        'type': 'bearer_token',
        'token': os.getenv('API_TOKEN', '')
    }
}

# Database Configuration (for future enhancement)
DATABASE_CONFIG = {
    'type': os.getenv('DB_TYPE', 'sqlite'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'name': os.getenv('DB_NAME', 'procurement_dashboard'),
    'username': os.getenv('DB_USERNAME', ''),
    'password': os.getenv('DB_PASSWORD', ''),
    'connection_pool_size': 5,
    'max_overflow': 10
}

# Security Configuration
SECURITY_CONFIG = {
    'session_timeout': 3600,  # 1 hour
    'max_login_attempts': 3,
    'password_min_length': 8,
    'require_https': os.getenv('REQUIRE_HTTPS', 'False').lower() == 'true',
    'allowed_hosts': os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(','),
    'cors_origins': os.getenv('CORS_ORIGINS', 'http://localhost:8501').split(',')
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_path': os.getenv('LOG_FILE', os.path.join(BASE_DIR, 'logs', 'dashboard.log')),
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
    'console_output': True
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'cache_size': 1000,  # Maximum number of cached items
    'cache_ttl': 3600,   # Cache time-to-live in seconds
    'max_concurrent_users': 50,
    'request_timeout': 30,
    'chunk_size': 1000,  # For processing large datasets
    'memory_limit_mb': 1024
}

# Feature Flags
FEATURE_FLAGS = {
    'enable_advanced_analytics': True,
    'enable_email_notifications': False,
    'enable_user_authentication': False,
    'enable_data_export': True,
    'enable_real_time_updates': False,
    'enable_ml_predictions': False,
    'enable_multi_language': False,
    'enable_custom_themes': False
}

# Development Configuration
DEV_CONFIG = {
    'debug_mode': os.getenv('DEBUG', 'False').lower() == 'true',
    'auto_reload': True,
    'show_profiling': False,
    'mock_external_apis': True,
    'test_data_mode': os.getenv('TEST_DATA_MODE', 'False').lower() == 'true'
}

# Environment Configuration
def get_environment() -> str:
    """Get current environment."""
    return os.getenv('ENVIRONMENT', 'development')

def is_production() -> bool:
    """Check if running in production."""
    return get_environment() == 'production'

def is_development() -> bool:
    """Check if running in development."""
    return get_environment() == 'development'

def is_testing() -> bool:
    """Check if running in testing mode."""
    return get_environment() == 'testing'

# Configuration Validation
def validate_config() -> Dict[str, Any]:
    """Validate configuration settings."""
    validation_results = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    # Check required directories
    required_dirs = [DATA_DIR, DASHBOARD_DIR, NOTEBOOKS_DIR]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            validation_results['errors'].append(f"Required directory missing: {dir_path}")
            validation_results['is_valid'] = False
    
    # Check data files
    required_files = [SAMPLE_DATA_FILE]
    for file_path in required_files:
        if not os.path.exists(file_path):
            validation_results['warnings'].append(f"Sample data file missing: {file_path}")
    
    # Check environment variables
    if is_production():
        required_env_vars = ['EMAIL_SENDER', 'EMAIL_PASSWORD', 'DB_PASSWORD']
        for env_var in required_env_vars:
            if not os.getenv(env_var):
                validation_results['errors'].append(f"Required environment variable missing: {env_var}")
                validation_results['is_valid'] = False
    
    return validation_results

# Configuration Summary
def get_config_summary() -> Dict[str, Any]:
    """Get configuration summary for display."""
    return {
        'project': {
            'name': PROJECT_NAME,
            'version': VERSION,
            'environment': get_environment()
        },
        'paths': {
            'data_dir': DATA_DIR,
            'dashboard_dir': DASHBOARD_DIR,
            'notebooks_dir': NOTEBOOKS_DIR
        },
        'features': {
            'enabled': [k for k, v in FEATURE_FLAGS.items() if v],
            'disabled': [k for k, v in FEATURE_FLAGS.items() if not v]
        },
        'data': {
            'sample_file': SAMPLE_DATA_FILE,
            'supported_formats': DATA_CONFIG['supported_formats']
        }
    }

# Initialize configuration
def init_config():
    """Initialize configuration settings."""
    # Create necessary directories
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
    
    # Validate configuration
    validation = validate_config()
    if not validation['is_valid']:
        print("Configuration validation failed:")
        for error in validation['errors']:
            print(f"  ERROR: {error}")
    
    if validation['warnings']:
        print("Configuration warnings:")
        for warning in validation['warnings']:
            print(f"  WARNING: {warning}")
    
    return validation

# Export main configuration variables
__all__ = [
    'PROJECT_NAME', 'VERSION', 'AUTHOR',
    'BASE_DIR', 'DATA_DIR', 'DASHBOARD_DIR', 'NOTEBOOKS_DIR',
    'DASHBOARD_CONFIG', 'DATA_CONFIG', 'ANALYTICS_CONFIG', 'VIZ_CONFIG',
    'DEPARTMENTS', 'CATEGORIES', 'ORDER_STATUSES', 'PRIORITIES',
    'FEATURE_FLAGS', 'get_environment', 'is_production', 'is_development',
    'validate_config', 'get_config_summary', 'init_config'
]
