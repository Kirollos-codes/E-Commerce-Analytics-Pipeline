# E-Commerce Sales Analytics ETL Pipeline

A Python ETL pipeline that processes e-commerce sales data and generates interactive visualizations.

## Features

- Extracts data from multiple CSV files (customers, products, orders)
- Cleans and transforms data with automated quality checks
- Loads data into SQLite database with star schema design
- Creates 6 interactive HTML dashboards with Plotly

## Tech Stack

- Python 3.8+
- Pandas for data processing
- SQLite for database
- Plotly for visualizations

## Installation

```bash
# Clone the repository
git clone https://github.com/Kirollos-codes/E-Commerce-Analytics-Pipeline.git
cd E-Commerce-Analytics-Pipeline

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Generate sample data
python src/generate_data.py

# Run the complete pipeline
python main.py
```

This will create:
- SQLite database in `output/ecommerce.db`
- 6 HTML dashboards in `output/` directory

## Project Structure

```
├── src/
│   ├── generate_data.py    # Creates sample data
│   ├── extract.py          # Loads CSV files
│   ├── transform.py        # Cleans and transforms data
│   ├── load.py             # Creates database
│   └── visualize.py        # Generates charts
├── data/                   # Raw CSV files
├── output/                 # Database and dashboards
├── main.py                 # Runs the pipeline
└── requirements.txt        # Python packages
```

## Database Schema

**Star schema with 3 tables:**

- `dim_customers` - Customer information and segments
- `dim_products` - Product details and pricing
- `fact_sales` - Order transactions with metrics

## Visualizations

The pipeline creates these dashboards:

1. Monthly Revenue & Profit Trend
2. Category Performance Analysis
3. Customer Segment Distribution
4. Top 10 Products by Revenue
5. Revenue by Country
6. Summary Statistics

## Data Quality

The pipeline automatically:
- Removes duplicate records
- Fills missing values
- Validates data types
- Calculates profit margins and customer segments

## What I Learned

- Building end-to-end ETL pipelines
- Star schema database design
- Data quality handling techniques
- Creating interactive visualizations
