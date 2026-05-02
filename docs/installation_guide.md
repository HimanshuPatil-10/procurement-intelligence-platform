# Installation Guide

This guide provides detailed instructions for setting up the Procurement Intelligence Dashboard on your system.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 1GB free disk space
- **Network**: Internet connection for package installation

### Recommended Requirements
- **Operating System**: Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.9 or higher
- **RAM**: 8GB or more
- **Storage**: 5GB free disk space
- **Processor**: Multi-core processor recommended

## Installation Methods

### Method 1: Standard Installation (Recommended)

#### Step 1: Verify Python Installation
Open your terminal or command prompt and check your Python version:

```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from:
- **Windows**: https://www.python.org/downloads/
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: Use package manager (apt, yum, etc.)

#### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv procurement_dashboard_env

# Activate virtual environment
# Windows:
procurement_dashboard_env\Scripts\activate
# macOS/Linux:
source procurement_dashboard_env/bin/activate
```

#### Step 3: Download the Project
```bash
# If using git
git clone <repository-url>
cd procurement-intelligence-dashboard

# Or download and extract the ZIP file
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Run the Dashboard
```bash
streamlit run dashboard/app.py
```

The dashboard will open in your web browser at `http://localhost:8501`

### Method 2: Development Installation

For developers who want to modify the code:

#### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd procurement-intelligence-dashboard
```

#### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 3: Install Dependencies in Development Mode
```bash
pip install -r requirements.txt
pip install -e .
```

#### Step 4: Install Development Tools
```bash
pip install black flake8 pytest jupyter
```

#### Step 5: Run Tests
```bash
pytest
```

#### Step 6: Start Development Server
```bash
streamlit run dashboard/app.py --server.runOnSave true
```

## Package Dependencies

### Core Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualizations
- **matplotlib**: Static plotting

### Analytics Dependencies
- **scipy**: Scientific computing
- **scikit-learn**: Machine learning utilities
- **statsmodels**: Statistical modeling

### Jupyter Dependencies
- **jupyter**: Interactive notebooks
- **notebook**: Jupyter notebook interface
- **ipykernel**: Jupyter kernel for Python

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```bash
# Data directory
DATA_DIR=./data

# Log level
LOG_LEVEL=INFO

# Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Streamlit Configuration
Create or edit `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "localhost"
headless = false
runOnSave = true

[browser]
gatherUsageStats = false

[theme]
base = "light"
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## Troubleshooting

### Common Installation Issues

#### Issue 1: Python Version Incompatibility
**Error**: `ERROR: Package requires a different Python`
**Solution**: 
```bash
# Check your Python version
python --version

# Upgrade Python if needed
# Or use a compatible version
```

#### Issue 2: Permission Denied
**Error**: `Permission denied` during installation
**Solution**:
```bash
# Use user installation
pip install --user -r requirements.txt

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue 3: Network Issues
**Error**: Connection timeout during package installation
**Solution**:
```bash
# Use different package index
pip install -i https://pypi.org/simple/ -r requirements.txt

# Or use offline installation (download packages first)
```

#### Issue 4: Missing System Dependencies
**Error**: Microsoft Visual C++ build tools required (Windows)
**Solution**:
1. Install Microsoft C++ Build Tools
2. Or use pre-compiled wheels: `pip install --only-binary=all -r requirements.txt`

### Runtime Issues

#### Issue 1: Module Not Found
**Error**: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue 2: Port Already in Use
**Error**: `Port 8501 is already in use`
**Solution**:
```bash
# Use different port
streamlit run dashboard/app.py --server.port 8502

# Or kill existing process
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

#### Issue 3: Data Loading Errors
**Error**: `FileNotFoundError` or data parsing errors
**Solution**:
1. Check if data files exist in `data/` directory
2. Verify data file format and structure
3. Check file permissions

## Performance Optimization

### Memory Optimization
```bash
# Limit memory usage
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
export STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200
```

### Caching Configuration
```bash
# Clear cache if needed
streamlit cache clear

# Configure cache size
streamlit run dashboard/app.py --server.maxMessageSize 200
```

## Docker Installation (Optional)

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0"]
```

### Docker Commands
```bash
# Build image
docker build -t procurement-dashboard .

# Run container
docker run -p 8501:8501 procurement-dashboard

# Run with volume mount
docker run -p 8501:8501 -v $(pwd)/data:/app/data procurement-dashboard
```

## Verification

### Test Installation
Run these commands to verify your installation:

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep streamlit

# Test Streamlit
streamlit hello

# Run dashboard
streamlit run dashboard/app.py
```

### Expected Results
- Streamlit hello page loads successfully
- Dashboard opens at http://localhost:8501
- All visualizations render correctly
- Data loads without errors
- Analytics functions work properly

## Next Steps

After successful installation:

1. **Explore the Dashboard**: Navigate through different sections
2. **Load Your Data**: Replace sample data with your procurement data
3. **Run Jupyter Notebooks**: Execute data analysis notebooks
4. **Customize Visualizations**: Modify charts and analytics as needed
5. **Set Up Automation**: Configure scheduled data refreshes

## Support Resources

- **Documentation**: Check the main README.md
- **Examples**: Review Jupyter notebooks for usage examples
- **Community**: Streamlit community forums
- **Issues**: Report bugs via GitHub issues

## Security Considerations

- **Data Privacy**: Ensure sensitive procurement data is properly secured
- **Network Security**: Use HTTPS in production environments
- **Access Control**: Implement authentication for production deployments
- **Input Validation**: Validate all user inputs and data sources

---

For additional help, refer to the main project documentation or create an issue in the repository.
