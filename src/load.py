import sqlite3
import pandas as pd
from datetime import datetime
import os

class DataLoader:
    def __init__(self, db_path='output/ecommerce.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        
    def create_schema(self):
        print("\nCreating database schema...")
        cur = self.conn.cursor()
        
        cur.execute("DROP TABLE IF EXISTS dim_customers")
        cur.execute("DROP TABLE IF EXISTS dim_products")
        cur.execute("DROP TABLE IF EXISTS fact_sales")
        
        cur.execute("""
            CREATE TABLE dim_customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT,
                email TEXT,
                registration_date DATE,
                country TEXT,
                customer_segment TEXT,
                days_since_registration INTEGER
            )
        """)
        
        cur.execute("""
            CREATE TABLE dim_products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                base_price REAL,
                cost REAL,
                profit_margin REAL,
                price_tier TEXT
            )
        """)
        
        cur.execute("""
            CREATE TABLE fact_sales (
                order_id INTEGER,
                customer_id INTEGER,
                product_id INTEGER,
                order_date DATE,
                order_month TEXT,
                order_year INTEGER,
                order_quarter INTEGER,
                day_of_week TEXT,
                quantity INTEGER,
                unit_price REAL,
                total_amount REAL,
                shipping_cost REAL,
                total_order_value REAL,
                status TEXT,
                category TEXT,
                customer_segment TEXT,
                country TEXT,
                price_tier TEXT,
                revenue REAL,
                cost_of_goods REAL,
                gross_profit REAL
            )
        """)
        
        self.conn.commit()
    
    def load_table(self, df, table_name, columns):
        df[columns].to_sql(table_name, self.conn, if_exists='append', index=False)
        print(f"  Loaded {len(df)} records into {table_name}")
        return len(df)
    
    def create_indexes(self):
        cur = self.conn.cursor()
        cur.execute("CREATE INDEX idx_sales_date ON fact_sales(order_date)")
        cur.execute("CREATE INDEX idx_sales_customer ON fact_sales(customer_id)")
        cur.execute("CREATE INDEX idx_sales_product ON fact_sales(product_id)")
        self.conn.commit()
    
    def load_all(self, data):
        print("\n--- LOAD ---")
        
        self.create_schema()
        
        self.load_table(data['customers'], 'dim_customers', 
                       ['customer_id', 'customer_name', 'email', 'registration_date',
                        'country', 'customer_segment', 'days_since_registration'])
        
        self.load_table(data['products'], 'dim_products',
                       ['product_id', 'product_name', 'category', 'base_price',
                        'cost', 'profit_margin', 'price_tier'])
        
        df = data['fact_sales'].copy()
        df['order_month'] = df['order_month'].astype(str)
        self.load_table(df, 'fact_sales', df.columns.tolist())
        
        self.create_indexes()
        
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM fact_sales WHERE status = 'Completed'")
        completed = cur.fetchone()[0]
        
        cur.execute("SELECT SUM(revenue), SUM(gross_profit) FROM fact_sales WHERE status = 'Completed'")
        rev, profit = cur.fetchone()
        
        print(f"\nDatabase summary:")
        print(f"  {completed:,} completed orders")
        print(f"  ${rev:,.2f} total revenue")
        print(f"  ${profit:,.2f} total profit")
        print(f"\nSaved to: {self.db_path}")
        
        self.conn.close()

if __name__ == "__main__":
    from extract import DataExtractor
    from transform import DataTransformer
    
    extractor = DataExtractor()
    raw = extractor.extract_all()
    
    transformer = DataTransformer()
    clean = transformer.transform_all(raw)
    
    loader = DataLoader()
    loader.load_all(clean)
