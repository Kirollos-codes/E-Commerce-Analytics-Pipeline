# E-Commerce Sales Analytics ETL Pipeline

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0.3-green.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.17.0-orange.svg)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-grade ETL (Extract, Transform, Load) pipeline for processing and analyzing e-commerce sales data. Features automated data quality checks, star schema database design, and interactive visualizations.

![Pipeline Architecture](https://img.shields.io/badge/Architecture-ETL%20Pipeline-brightgreen)

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Visualizations](#visualizations)
- [Data Quality](#data-quality)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Data Processing
- **Multi-table ETL Pipeline**: Processes customers, products, and orders data
- **Automated Data Quality**: Handles duplicates, missing values, and outliers
- **Feature Engineering**: Creates derived metrics (profit margins, customer segments, price tiers)
- **Data Validation**: Schema validation and integrity checks at each stage

### Database Design
- **Star Schema Architecture**: Optimized for analytics with dimension and fact tables
- **Database Indexes**: Performance optimization on key columns
- **Relational Integrity**: Proper foreign key relationships

### Analytics & Visualization
- **Interactive Dashboards**: 6 Plotly-powered HTML visualizations
- **Business Metrics**: Revenue, profit, customer segments, geographic analysis
- **Automated Reporting**: Summary statistics and KPI tracking

---

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   EXTRACT   │ ───> │  TRANSFORM  │ ───> │    LOAD     │ ───> │  VISUALIZE  │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
      │                     │                     │                     │
  Raw CSV Data      Data Cleaning          SQLite DB           Interactive Charts
  3 Tables          Feature Creation       Star Schema          HTML Dashboards
```

**Pipeline Flow:**
1. **Extract**: Load raw data from CSV files (customers, products, orders)
2. **Transform**: Clean data, create features, build fact table
3. **Load**: Create star schema database with indexes
4. **Visualize**: Generate interactive Plotly dashboards

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Pandas** | Data manipulation and transformation |
| **NumPy** | Numerical operations |
| **SQLite** | Relational database |
| **Plotly** | Interactive visualizations |
| **Kaleido** | Static image export (optional) |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Kirollos-codes/E-Commerce-Analytics-Pipeline.git
cd E-Commerce-Analytics-Pipeline
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Quick Start

```bash
# Step 1: Generate sample data
python src/generate_data.py

# Step 2: Run the complete ETL pipeline
python main.py
```

### Running Individual Modules

```bash
# Extract only
python src/extract.py

# Transform only (requires extracted data)
python src/transform.py

# Load only (requires transformed data)
python src/load.py

# Visualize only (requires loaded database)
python src/visualize.py
```

### Expected Output

```
==================================================
E-COMMERCE ANALYTICS ETL PIPELINE
==================================================

--- EXTRACT ---
Extracted 500 customers
Extracted 50 products
Extracted 2010 orders

--- TRANSFORM ---
Cleaning customers...
  Removed 0 duplicates -> 500 records
Cleaning products...
  Added profit metrics -> 50 records
Cleaning orders...
  Filled 20 missing shipping costs
  Removed 10 invalid records -> 2000 records
Building fact table...
  Created 2000 sales records
  Total revenue: $250,482.35
  Total profit: $125,241.18

--- LOAD ---
Creating database schema...
  Loaded 500 records into dim_customers
  Loaded 50 records into dim_products
  Loaded 2000 records into fact_sales

Database summary:
  1,700 completed orders
  $212,909.00 total revenue
  $106,454.50 total profit

Saved to: output/ecommerce.db

--- VISUALIZE ---
Generating visualizations...
  Created monthly_revenue.html
  Created category_performance.html
  Created customer_segments.html
  Created top_products.html
  Created country_analysis.html
  Created summary_stats.html

All visualizations saved to 'output/' directory

==================================================
Pipeline completed successfully!
==================================================
```

---

## 📁 Project Structure

```
E-Commerce-Analytics-Pipeline/
│
├── src/
│   ├── generate_data.py      # Sample data generation
│   ├── extract.py             # Data extraction module
│   ├── transform.py           # Data transformation & cleaning
│   ├── load.py                # Database loading module
│   └── visualize.py           # Visualization generation
│
├── data/                      # Raw CSV data files (generated)
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
│
├── output/                    # Generated outputs
│   ├── ecommerce.db          # SQLite database
│   ├── monthly_revenue.html
│   ├── category_performance.html
│   ├── customer_segments.html
│   ├── top_products.html
│   ├── country_analysis.html
│   └── summary_stats.html
│
├── main.py                    # Pipeline orchestration
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── LICENSE                    # MIT License

```

---

## 🗄️ Database Schema

### Star Schema Design

```sql
-- Dimension Tables
┌─────────────────┐
│ dim_customers   │
├─────────────────┤
│ customer_id (PK)│
│ customer_name   │
│ email           │
│ registration_date│
│ country         │
│ customer_segment│
│ days_since_reg  │
└─────────────────┘

┌─────────────────┐
│ dim_products    │
├─────────────────┤
│ product_id (PK) │
│ product_name    │
│ category        │
│ base_price      │
│ cost            │
│ profit_margin   │
│ price_tier      │
└─────────────────┘

-- Fact Table
┌─────────────────────────┐
│ fact_sales              │
├─────────────────────────┤
│ order_id                │
│ customer_id (FK)        │
│ product_id (FK)         │
│ order_date              │
│ order_month             │
│ order_year              │
│ order_quarter           │
│ day_of_week             │
│ quantity                │
│ unit_price              │
│ total_amount            │
│ shipping_cost           │
│ total_order_value       │
│ status                  │
│ category                │
│ customer_segment        │
│ country                 │
│ price_tier              │
│ revenue                 │
│ cost_of_goods           │
│ gross_profit            │
└─────────────────────────┘

-- Indexes
CREATE INDEX idx_sales_date ON fact_sales(order_date)
CREATE INDEX idx_sales_customer ON fact_sales(customer_id)
CREATE INDEX idx_sales_product ON fact_sales(product_id)
```

---

## 📊 Visualizations

The pipeline generates 6 interactive HTML dashboards:

### 1. **Monthly Revenue & Profit Trend**
- Time series analysis of revenue and profit
- Identifies seasonal patterns and growth trends
- Interactive hover tooltips with exact values

### 2. **Category Performance Analysis**
- Side-by-side comparison of revenue and profit by category
- Identifies top-performing product categories
- Bar charts with color-coded metrics

### 3. **Customer Segment Distribution**
- Pie chart showing revenue by customer tier
- Segments: Premium, Standard, Basic
- Percentage breakdown of total revenue

### 4. **Top 10 Products by Revenue**
- Horizontal bar chart of best-selling products
- Includes category information
- Sorted by revenue performance

### 5. **Revenue by Country**
- Geographic revenue analysis
- Order count and average order value metrics
- Identifies key markets

### 6. **Summary Statistics Dashboard**
- Executive KPI summary
- Total customers, products, orders
- Revenue, profit, and margin metrics
- Clean tabular format

---

## 🔍 Data Quality

### Automated Quality Checks

| Issue | Solution | Method |
|-------|----------|--------|
| **Duplicate Records** | Removed | `drop_duplicates()` on order_id |
| **Missing Values** | Filled | Median imputation for shipping costs |
| **Invalid Records** | Filtered | Remove orders with value ≤ 0 |
| **Data Types** | Converted | Proper datetime parsing |
| **Country Names** | Standardized | USA → United States, UK → United Kingdom |

### Feature Engineering

**Customer Metrics:**
- Days since registration
- Customer lifetime value
- Customer segment classification

**Product Metrics:**
- Profit margin calculation: `(price - cost) / price * 100`
- Price tier classification: Budget, Mid-Range, Premium

**Order Metrics:**
- Total order value: `item_total + shipping`
- Gross profit: `revenue - cost_of_goods`
- Time-based dimensions: month, quarter, day of week

---

## 📈 Sample Insights

Based on generated sample data, the pipeline reveals:

- **Top Category**: Electronics generates 35% of total revenue
- **Customer Distribution**: 20% Premium, 50% Standard, 30% Basic
- **Average Order Value**: $125.24
- **Profit Margin**: ~50% average across all products
- **Peak Period**: Q3 shows highest sales volume
- **Geographic Concentration**: 40% of orders from United States

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Add data validation tests with pytest
- [ ] Implement incremental loading (process only new records)
- [ ] Add data quality monitoring dashboard
- [ ] Integrate with cloud databases (Snowflake, BigQuery)
- [ ] Create REST API for data access
- [ ] Add machine learning predictions (customer churn, demand forecasting)
- [ ] Implement real-time streaming with Apache Kafka
- [ ] Add Docker containerization
- [ ] Create CI/CD pipeline with GitHub Actions

### Scalability Considerations
- **Database**: Migrate to PostgreSQL or Snowflake for larger datasets
- **Processing**: Use Apache Spark for distributed processing
- **Orchestration**: Implement Apache Airflow for scheduling
- **Monitoring**: Add logging and alerting with ELK stack

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Kirollos**
- GitHub: [@Kirollos-codes](https://github.com/Kirollos-codes)
- Project Link: [E-Commerce-Analytics-Pipeline](https://github.com/Kirollos-codes/E-Commerce-Analytics-Pipeline)

---


---

## 📚 Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Star Schema Design Guide](https://en.wikipedia.org/wiki/Star_schema)

---

**⭐ If you find this project useful, please consider giving it a star!**
