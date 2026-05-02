# Data Directory

This directory contains sample datasets and data files for the Procurement Intelligence Dashboard.

## Files Description

### Sample Datasets

1. **sample_procurement_data.csv**
   - Contains sample procurement transaction data
   - Fields: Order_ID, Date, Delivery_Date, Department, Supplier, Category, Item_Description, Quantity, Unit_Price, Amount, Status, Priority, Lead_Time, Approved_By, Contract_ID
   - Size: 50 sample records
   - Date Range: January 2024 - April 2024

2. **supplier_master_data.csv**
   - Master data for suppliers
   - Fields: Supplier_ID, Supplier_Name, Category, Contact_Person, Email, Phone, Address, City, State, Country, Contract_Start_Date, Contract_End_Date, Payment_Terms, Rating, Active
   - Size: 8 suppliers
   - Includes contact information and contract details

3. **department_budget.csv**
   - Budget vs actual spending by department and quarter
   - Fields: Department, Quarter, Budget, Actual_Spend, Variance, Variance_Percentage
   - Size: 32 records (8 departments × 4 quarters)
   - Covers fiscal year 2024

### Data Structure

#### Departments
- IT
- Marketing
- Operations
- Sales
- HR
- Finance
- Legal

#### Suppliers
- TechCorp Solutions (Hardware)
- OfficeSupply Co. (Office Supplies)
- Marketing Pro (Marketing Materials)
- Cloud Services Inc. (Services)
- Hardware Hub (Hardware)
- Software Systems (Software)
- Consulting Group (Services)
- Facility Management (Services)

#### Categories
- Hardware
- Software
- Services
- Office Supplies
- Marketing Materials
- Consulting

#### Order Status
- Completed
- Pending
- Cancelled
- On Hold

#### Priority Levels
- High
- Medium
- Low

## Usage

These datasets can be used to:
1. Test the data processing modules in `src/data_processor.py`
2. Run analytics using `src/analytics.py`
3. Create visualizations with `src/visualizations.py`
4. Populate the Streamlit dashboard
5. Explore data in Jupyter notebooks

## Data Generation

The sample data was generated to represent realistic procurement scenarios:
- Order amounts range from $1,500 to $16,000
- Lead times vary from 10 to 34 days
- Multiple departments and suppliers are represented
- Different order statuses and priorities are included
- Budget vs actual spending shows realistic variances

## Data Quality

- All records have complete information
- Dates are consistent and logical
- Amount calculations are accurate (Quantity × Unit_Price = Amount)
- Lead times are calculated correctly (Delivery_Date - Order_Date)
- Supplier and department names are consistent across files

## Extending the Data

To add more data:
1. Follow the same column structure and naming conventions
2. Maintain data consistency across related fields
3. Use realistic values for amounts and dates
4. Ensure referential integrity between related files

## Data Privacy

This is sample data only. No real company or personal information is included.
