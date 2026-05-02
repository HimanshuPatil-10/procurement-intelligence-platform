# Procurement Intelligence Platform

[![CI/CD](https://github.com/yourusername/procurement-intelligence-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/procurement-intelligence-dashboard/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A **production-ready** procurement intelligence platform built with **FastAPI** backend and **Streamlit** frontend, featuring ML-powered analytics, comprehensive testing, and CI/CD pipeline.

**🎯 Perfect for: Data Engineering | Backend Development | Analytics | DevOps portfolios**

## 🏗️ Architecture

```
┌─────────────────┐     HTTP/REST     ┌──────────────────┐
│   Streamlit      │ ←──────────────→ │   FastAPI        │
│   Dashboard      │      JSON API     │   Backend        │
│   (Frontend)     │                   │   (API Layer)    │
└─────────────────┘                   └────────┬─────────┘
                                                 │
                                        ┌────────▼─────────┐
                                        │  SQLAlchemy ORM   │
                                        │  + SQLite DB      │
                                        └────────┬─────────┘
                                                 │
                                        ┌────────▼─────────┐
                                        │  Analytics Engine │
                                        │  Pandas/NumPy/SciPy│
                                        └──────────────────┘
```

**Key Technologies:**
- **Backend:** FastAPI + SQLAlchemy + Pydantic
- **Frontend:** Streamlit
- **Database:** SQLite (production-ready for PostgreSQL)
- **Testing:** pytest + coverage + CI/CD
- **Deployment:** Docker + Docker Compose

## 🚀 Features

### API Backend (FastAPI)
- **RESTful API Design**: Clean, documented API following REST conventions
- **Automatic API Documentation**: Swagger UI at `/docs`, ReDoc at `/redoc`
- **Data Persistence**: SQLAlchemy ORM with SQLite database
- **Request/Response Validation**: Pydantic schemas for type safety
- **Health Monitoring**: `/health` endpoint for system status

**Available Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | System health check |
| GET | `/orders` | Get procurement orders with filtering |
| GET | `/filters/options` | Get filter dropdown options |
| GET | `/kpis` | Key performance indicators |
| GET | `/metrics` | Comprehensive metrics |
| POST | `/analytics/forecast` | Spending forecast with confidence intervals |
| GET | `/analytics/suppliers` | Supplier performance analysis |
| GET | `/analytics/risks` | Risk assessment |
| GET | `/analytics/opportunities` | Cost optimization opportunities |
| GET | `/analytics/insights` | Comprehensive insights report |

### Core Dashboard
- **Real-time KPIs**: Track total spend, average order value, total orders, and lead times
- **Interactive Filtering**: Filter by date range, department, supplier, category, and order status
- **Dynamic Visualizations**: Department spend breakdown, monthly trends, supplier analysis, and category distribution
- **Data Export**: Download filtered data in CSV format

### Advanced Analytics
- **Spending Forecast**: Predict future spending with confidence intervals using time series analysis
- **Supplier Performance Analysis**: Comprehensive supplier evaluation with performance scoring
- **Risk Assessment**: Identify and mitigate procurement risks across multiple dimensions
- **Optimization Opportunities**: AI-powered recommendations for cost savings and efficiency improvements

### Data Processing
- **Automated Data Cleaning**: Handle missing values, duplicates, and data validation
- **Sample Data Generation**: Generate realistic procurement data for testing and demonstration
- **Multiple Data Sources**: Support for CSV, Excel, and JSON formats

## 📁 Project Structure

```
procurement-intelligence-dashboard/
├── api/                        # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                 # API endpoints & application
│   ├── models.py               # SQLAlchemy database models
│   └── schemas.py              # Pydantic request/response schemas
├── dashboard/                  # Streamlit Frontend
│   └── app.py                  # Dashboard application
├── src/                        # Core Analytics Engine
│   ├── __init__.py
│   ├── data_processor.py      # Data processing & ETL
│   ├── analytics.py            # ML-powered analytics
│   ├── visualizations.py       # Chart generation
│   ├── utils.py                # Utility functions
│   └── config.py               # Configuration management
├── tests/                      # Comprehensive Test Suite
│   ├── conftest.py             # Pytest fixtures
│   ├── test_data_processor.py  # Unit tests
│   ├── test_analytics.py        # Unit tests
│   └── test_api.py             # Integration tests
├── notebooks/                  # Jupyter Notebooks
│   ├── data_exploration.ipynb
│   └── supplier_analysis.ipynb
├── data/                       # Sample Datasets
│   ├── sample_procurement_data.csv
│   ├── supplier_master_data.csv
│   └── department_budget.csv
├── .github/workflows/          # CI/CD Pipeline
│   └── ci.yml
├── Dockerfile                  # Docker containerization
├── docker-compose.yml          # Multi-service orchestration
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/procurement-intelligence-dashboard.git
cd procurement-intelligence-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests to verify installation
pytest tests/ -v
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access API at: http://localhost:8000
# Access Dashboard at: http://localhost:8501
```
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd procurement-intelligence-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run dashboard/app.py
   ```

4. **Access the dashboard**
   Open your web browser and navigate to `http://localhost:8501`

## 📊 Usage Guide

### Getting Started

1. **Launch the Dashboard**: Run the Streamlit app using the command above
2. **Load Data**: The dashboard automatically loads sample data. You can replace it with your own data
3. **Apply Filters**: Use the sidebar filters to focus on specific time periods, departments, or suppliers
4. **Generate Insights**: Click "Generate Insights" to run advanced analytics

### Dashboard Features

#### Sidebar Controls
- **Date Range Filter**: Select specific time periods for analysis
- **Department Filter**: Focus on specific departments
- **Supplier Filter**: Analyze individual suppliers or all suppliers
- **Category Filter**: Filter by procurement categories
- **Status Filter**: View orders by completion status
- **Generate Insights**: Run comprehensive analytics

#### Main Dashboard Sections
1. **KPIs**: Real-time performance metrics
2. **Department Analysis**: Spending breakdown by department
3. **Trend Analysis**: Monthly spending patterns
4. **Supplier Performance**: Top suppliers and spending patterns
5. **Category Distribution**: Spending across procurement categories
6. **Transaction Table**: Detailed transaction records

#### Advanced Analytics Tabs
1. **Forecast**: Spending predictions with confidence intervals
2. **Suppliers**: Performance rankings and analysis
3. **Risks**: Risk assessment and mitigation strategies
4. **Opportunities**: Optimization recommendations

## 📈 Data Requirements

### Supported Data Formats
- **CSV** (Comma Separated Values)
- **Excel** (.xlsx, .xls)
- **JSON** (JavaScript Object Notation)

### Required Columns
For optimal functionality, your procurement data should include:
- `Date`: Order date
- `Department`: Department name
- `Supplier`: Supplier name
- `Category`: Procurement category
- `Amount`: Order amount
- `Status`: Order status (Completed, Pending, etc.)
- `Lead_Time`: Delivery lead time in days

### Optional Columns
- `Order_ID`: Unique order identifier
- `Delivery_Date`: Expected delivery date
- `Item_Description`: Item or service description
- `Quantity`: Order quantity
- `Unit_Price`: Price per unit
- `Priority`: Order priority level
- `Approved_By`: Approving authority
- `Contract_ID`: Associated contract identifier

## 🔧 Customization

### Adding Your Own Data
1. Place your data file in the `data/` directory
2. Update the data loading function in `dashboard/app.py`
3. Ensure column names match the required format

### Extending Analytics
1. Add new analysis functions to `src/analytics.py`
2. Create new visualizations in `src/visualizations.py`
3. Update the dashboard to display new insights

### Customizing Visualizations
- Modify chart configurations in `src/visualizations.py`
- Update color schemes and styling in `dashboard/app.py`
- Add new chart types as needed

## 📚 Jupyter Notebooks

### Data Exploration (`notebooks/data_exploration.ipynb`)
- Comprehensive data analysis
- Quality assessment and validation
- Statistical analysis and correlations
- Time series exploration

### Supplier Analysis (`notebooks/supplier_analysis.ipynb`)
- Supplier performance evaluation
- Risk assessment and segmentation
- Cost analysis and optimization
- Recommendation generation

## 🎯 Key Analytics Features

### Spending Forecast
- **Method**: Moving average with linear trend
- **Confidence Intervals**: 95% confidence bounds
- **Model Validation**: R-squared and p-value metrics

### Supplier Performance
- **Performance Scoring**: Composite score based on reliability, speed, volume, and consistency
- **Risk Assessment**: Multi-dimensional risk evaluation
- **Segmentation**: Strategic, Critical, Preferred, Approved, and Development categories

### Risk Analysis
- **Dependency Risk**: Supplier concentration analysis
- **Performance Risk**: Completion rate and lead time evaluation
- **Price Volatility**: Market price fluctuation assessment
- **Delivery Risk**: Supply chain disruption analysis

### Optimization Opportunities
- **Price Standardization**: Identify price variations for similar items
- **Supplier Diversification**: Reduce dependency on single suppliers
- **Order Batching**: Consolidate small orders for efficiency
- **Lead Time Optimization**: Improve delivery performance

## 🔍 Technical Details

### Architecture
- **Frontend**: Streamlit web framework
- **Backend**: Python data processing with pandas and numpy
- **Analytics**: Statistical analysis with scipy and scikit-learn
- **Visualization**: Plotly for interactive charts
- **Data Storage**: CSV files (easily replaceable with databases)

### Performance
- **Caching**: Streamlit caching for improved performance
- **Lazy Loading**: Analytics generated on-demand
- **Memory Optimization**: Efficient data processing techniques

## 🐛 Troubleshooting

### Common Issues

1. **Module Not Found Error**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

2. **Data Loading Issues**
   - Verify data file format and structure
   - Check for missing required columns
   - Ensure file paths are correct

3. **Dashboard Not Loading**
   - Check if port 8501 is available
   - Try running with a different port: `streamlit run dashboard/app.py --server.port 8502`

4. **Analytics Errors**
   - Ensure sufficient data volume for analysis
   - Check data quality and completeness
   - Review error messages in the dashboard

### Performance Tips
- Use smaller date ranges for faster analysis
- Clear cache regularly: `streamlit cache clear`
- Limit data volume for real-time analytics

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a virtual environment
3. Install development dependencies
4. Make changes and test thoroughly
5. Submit pull requests

### Code Standards
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include error handling
- Write unit tests for new features

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the Jupyter notebooks for examples
3. Examine the data requirements section
4. Verify your data format and structure

## 🚀 Future Enhancements

### Planned Features
- **Real-time Data Integration**: Connect to live procurement systems
- **Machine Learning**: Advanced predictive analytics
- **Multi-user Support**: Role-based access control
- **Alert System**: Automated notifications for risks and opportunities
- **Mobile Optimization**: Responsive design for mobile devices
- **Database Integration**: Support for SQL and NoSQL databases
- **API Integration**: Connect to external procurement systems
- **Advanced Reporting**: Custom report generation and scheduling

### Scalability Improvements
- **Cloud Deployment**: AWS, Azure, or Google Cloud integration
- **Microservices Architecture**: Modular service design
- **Load Balancing**: Handle multiple concurrent users
- **Data Pipeline**: ETL processes for large datasets

---

**Built with ❤️ using Streamlit, Python, and modern data science tools**
