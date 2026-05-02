# User Guide

This comprehensive guide helps you navigate and use the Procurement Intelligence Dashboard effectively.

## Getting Started

### Launching the Dashboard

1. **Open Terminal/Command Prompt**
   - Windows: Open Command Prompt or PowerShell
   - macOS: Open Terminal
   - Linux: Open Terminal

2. **Navigate to Project Directory**
   ```bash
   cd procurement-intelligence-dashboard
   ```

3. **Run the Dashboard**
   ```bash
   streamlit run dashboard/app.py
   ```

4. **Access in Browser**
   - Open your web browser
   - Go to `http://localhost:8501`
   - The dashboard will load automatically

### First-Time Setup

1. **Data Loading**: The dashboard automatically loads sample data
2. **Explore Features**: Take a tour of the different sections
3. **Apply Filters**: Use sidebar filters to explore data
4. **Generate Insights**: Click "Generate Insights" for advanced analytics

## Dashboard Overview

### Main Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    Header & Title                           │
├─────────────────┬───────────────────────────────────────────┤
│                 │                                           │
│   Sidebar       │            Main Content                   │
│   Controls      │                                           │
│                 │                                           │
│                 │                                           │
│                 │                                           │
└─────────────────┴───────────────────────────────────────────┘
```

### Key Sections

1. **Sidebar Controls**: Filters and analytics options
2. **KPIs**: Key performance indicators
3. **Visualizations**: Charts and graphs
4. **Data Table**: Detailed transaction records
5. **Advanced Analytics**: In-depth insights and recommendations

## Sidebar Controls

### Date Range Filter
- **Purpose**: Analyze specific time periods
- **Usage**: 
  - Click on the date picker
  - Select start and end dates
  - Dashboard updates automatically

### Department Filter
- **Options**: All Departments, IT, Operations, Marketing, Sales, HR, Finance, Legal
- **Usage**: Select a department to focus analysis
- **Impact**: All charts and metrics update for selected department

### Supplier Filter
- **Dynamic List**: Populated from your data
- **Usage**: Select "All Suppliers" or specific supplier
- **Benefit**: Analyze individual supplier performance

### Category Filter
- **Categories**: Hardware, Software, Services, Office Supplies, Marketing Materials, Consulting
- **Usage**: Filter by procurement category
- **Analysis**: Category-specific spending patterns

### Status Filter
- **Statuses**: All Statuses, Completed, Pending, Cancelled, On Hold
- **Usage**: View orders by completion status
- **Tracking**: Monitor order fulfillment

### Generate Insights Button
- **Purpose**: Run advanced analytics
- **Process**: 
  - Click the button
  - Wait for analysis to complete
  - View results in new tabs below

## Main Dashboard Sections

### Key Performance Indicators (KPIs)

Four main metrics displayed at the top:

1. **Total Spend**
   - Definition: Sum of all order amounts
   - Filter: Updates based on applied filters
   - Delta: Shows percentage change from unfiltered data

2. **Average Order Value**
   - Definition: Mean order amount
   - Calculation: Total Spend ÷ Number of Orders
   - Insight: Helps understand typical transaction size

3. **Total Orders**
   - Definition: Count of all orders
   - Filter: Updates with applied filters
   - Use: Track order volume

4. **Average Lead Time**
   - Definition: Mean delivery time in days
   - Importance: Supply chain efficiency metric
   - Target: Lower values indicate better performance

### Visualizations

#### Department Spending Pie Chart
- **Location**: Top left visualization
- **Purpose**: Show spending distribution across departments
- **Interaction**: Hover for detailed percentages
- **Insight**: Identify which departments spend the most

#### Monthly Spending Trend Line Chart
- **Location**: Top right visualization
- **Purpose**: Show spending patterns over time
- **Features**: 
  - Line chart with markers
  - Interactive hover tooltips
  - Time series analysis

#### Top Suppliers Bar Chart
- **Location**: Bottom left visualization
- **Purpose**: Rank suppliers by total spend
- **Features**:
  - Horizontal bar chart
  - Top 10 suppliers
  - Sorted by spend amount

#### Category Distribution Sunburst
- **Location**: Bottom right visualization
- **Purpose**: Show hierarchical spending by category
- **Features**:
  - Interactive sunburst diagram
  - Proportional representation
  - Click to drill down

### Data Table

#### Recent Transactions
- **Purpose**: View detailed order information
- **Columns**: Date, Department, Supplier, Category, Amount, Status
- **Features**:
  - Sortable columns
  - Scrollable for large datasets
  - Shows 10 most recent orders

#### Download Functionality
- **Button**: "📥 Download Filtered Data"
- **Format**: CSV file
- **Content**: Currently filtered data
- **Use**: Export data for external analysis

## Advanced Analytics

### Accessing Advanced Analytics

1. **Generate Insights**: Click the button in sidebar
2. **Wait for Processing**: Analysis may take a few seconds
3. **View Results**: Four new tabs appear below main dashboard

### Analytics Tabs

#### 📊 Forecast Tab

**Spending Forecast Chart**
- **Historical Data**: Blue line showing past spending
- **Forecast**: Orange dashed line showing predictions
- **Confidence Interval**: Shaded area showing uncertainty bounds
- **Time Period**: 12-month forecast

**Forecast Metrics**
- **Model R²**: Statistical measure of model accuracy (0-1, higher is better)
- **Next Month Forecast**: Predicted spending for next month
- **Forecast Method**: Statistical approach used

**Usage Tips**:
- Use forecasts for budget planning
- Consider confidence intervals for risk assessment
- Higher R² values indicate more reliable predictions

#### 🏆 Suppliers Tab

**Top Performing Suppliers**
- **Criteria**: Composite performance score
- **Factors**: Reliability, speed, volume, consistency
- **Display**: List of best-performing suppliers

**Suppliers Needing Attention**
- **Purpose**: Identify underperforming suppliers
- **Action**: Review and improve supplier relationships
- **Impact**: Overall procurement efficiency

**Supplier Metrics Table**
- **Columns**: Performance metrics for each supplier
- **Data**: Spend, orders, lead times, completion rates
- **Use**: Detailed supplier analysis

#### ⚠️ Risks Tab

**Overall Risk Level**
- **Indicators**: 🟢 Low, 🟡 Medium, 🔴 High
- **Calculation**: Based on multiple risk factors
- **Action**: High risks require immediate attention

**High Priority Risks**
- **Display**: Expandable risk details
- **Information**:
  - Risk type and entity
  - Description of the risk
  - Mitigation strategies

**All Identified Risks**
- **Table**: Complete risk inventory
- **Columns**: Risk type, entity, level, description, mitigation
- **Use**: Comprehensive risk management

#### 💡 Opportunities Tab

**Summary Metrics**
- **Total Opportunities**: Count of optimization suggestions
- **Priority Areas**: Most important improvement categories

**Opportunity Details**
- **Expandable Sections**: Click each opportunity for details
- **Information Provided**:
  - Opportunity type
  - Detailed description
  - Potential savings or benefits
  - Implementation recommendations

**Common Opportunity Types**:
- Price Standardization
- Supplier Diversification
- Order Batching
- Lead Time Optimization

## Data Analysis Workflow

### Step-by-Step Analysis

1. **Define Analysis Scope**
   - Select date range of interest
   - Choose relevant departments or suppliers
   - Apply category or status filters

2. **Review KPIs**
   - Check total spending patterns
   - Analyze order values and quantities
   - Monitor lead time performance

3. **Explore Visualizations**
   - Identify department spending patterns
   - Analyze monthly trends
   - Review supplier performance
   - Examine category distributions

4. **Generate Advanced Insights**
   - Click "Generate Insights"
   - Review spending forecasts
   - Analyze supplier performance
   - Assess identified risks
   - Evaluate optimization opportunities

5. **Export and Report**
   - Download filtered data
   - Take screenshots of key charts
   - Document findings and recommendations

### Analysis Examples

#### Example 1: Department Spending Review
1. **Filter**: Select specific department
2. **Analyze**: Review department KPIs and spending patterns
3. **Compare**: Use "All Departments" to compare performance
4. **Optimize**: Look for cost-saving opportunities

#### Example 2: Supplier Performance Evaluation
1. **Filter**: Select specific supplier
2. **Generate Insights**: Run advanced analytics
3. **Review**: Check supplier tab for performance metrics
4. **Action**: Identify improvement areas or relationship changes

#### Example 3: Budget Planning
1. **Set Date Range**: Select relevant planning period
2. **Generate Forecast**: Click "Generate Insights"
3. **Review Forecast**: Check forecast tab for predictions
4. **Plan**: Use insights for budget allocation

## Best Practices

### Data Quality
- **Regular Updates**: Keep data current for accurate insights
- **Consistent Formatting**: Maintain consistent data formats
- **Complete Information**: Ensure all required fields are populated
- **Validation**: Verify data accuracy before analysis

### Analysis Techniques
- **Start Broad**: Begin with overall patterns before drilling down
- **Compare Periods**: Use date ranges to compare time periods
- **Multiple Filters**: Combine filters for targeted analysis
- **Validate Insights**: Cross-check findings with domain knowledge

### Decision Making
- **Consider Context**: Factor in business context when interpreting results
- **Prioritize Actions**: Focus on high-impact opportunities first
- **Monitor Changes**: Track performance changes over time
- **Collaborate**: Share insights with relevant stakeholders

## Troubleshooting

### Common Issues

#### Dashboard Not Loading
- **Solution**: Check terminal for error messages
- **Check**: Internet connection and Python environment
- **Restart**: Stop and restart the Streamlit server

#### Data Not Displaying
- **Check**: Data files in the `data/` directory
- **Verify**: Data format and required columns
- **Refresh**: Reload the dashboard page

#### Analytics Not Working
- **Wait**: Advanced analytics may take time to process
- **Check**: Sufficient data volume (need minimum records)
- **Review**: Error messages in sidebar

#### Charts Not Updating
- **Check**: Applied filters
- **Verify**: Data contains relevant categories
- **Refresh**: Clear browser cache and reload

### Performance Tips

#### Improve Loading Speed
- **Use Smaller Date Ranges**: Limit analysis to specific periods
- **Apply Filters**: Reduce data volume with targeted filters
- **Clear Cache**: Periodically clear Streamlit cache

#### Handle Large Datasets
- **Sample Data**: Use data sampling for initial exploration
- **Incremental Analysis**: Analyze data in chunks
- **Background Processing**: Run analytics during off-peak hours

## Keyboard Shortcuts

### Streamlit Shortcuts
- **Ctrl + Enter**: Run current script
- **Ctrl + S**: Save changes
- **Ctrl + R**: Refresh dashboard
- **Esc**: Clear current input

### Browser Shortcuts
- **F5**: Refresh page
- **Ctrl + +**: Zoom in
- **Ctrl + -**: Zoom out
- **Ctrl + 0**: Reset zoom

## Mobile Usage

### Mobile Considerations
- **Responsive Design**: Dashboard adapts to screen size
- **Touch Interaction**: Charts support touch gestures
- **Limited Features**: Some advanced features work best on desktop

### Mobile Tips
- **Landscape Mode**: Better for viewing charts
- **Wi-Fi Connection**: Recommended for faster loading
- **Simplified Analysis**: Use basic filters on mobile

## Integration and Export

### Data Export
- **CSV Format**: Download filtered data
- **Timestamp**: Files include download timestamp
- **Filtered Data**: Only includes currently filtered data

### Screenshot Capture
- **Windows**: Win + Shift + S
- **macOS**: Cmd + Shift + 4
- **Use**: Capture charts for reports and presentations

### Report Generation
- **Combine Data**: Export data and screenshots
- **Document Insights**: Include analytics findings
- **Share Results**: Distribute to stakeholders

## Security and Privacy

### Data Security
- **Local Processing**: Data processed on your machine
- **No Cloud Upload**: Data never leaves your system
- **Secure Storage**: Keep data files in secure location

### Privacy Considerations
- **Sensitive Data**: Avoid sharing sensitive procurement data
- **Access Control**: Limit dashboard access to authorized users
- **Data Retention**: Follow your organization's data retention policies

---

For additional assistance, refer to the installation guide or project documentation.
