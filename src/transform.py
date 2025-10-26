import pandas as pd
import numpy as np
from datetime import datetime

class DataTransformer:
    def __init__(self):
        self.stats = {}
    
    def clean_customers(self, df):
        print("\nCleaning customers...")
        orig = len(df)
        df = df.drop_duplicates(subset=['customer_id'])
        
        df['country'] = df['country'].replace({'USA': 'United States', 'UK': 'United Kingdom'})
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        df['days_since_registration'] = (datetime.now() - df['registration_date']).dt.days
        
        print(f"  Removed {orig - len(df)} duplicates -> {len(df)} records")
        return df
    
    def clean_products(self, df):
        print("\nCleaning products...")
        df['profit_margin'] = ((df['base_price'] - df['cost']) / df['base_price'] * 100).round(2)
        df['price_tier'] = pd.cut(df['base_price'], bins=[0, 50, 150, 500], labels=['Budget', 'Mid-Range', 'Premium'])
        print(f"  Added profit metrics -> {len(df)} records")
        return df
    
    def clean_orders(self, df):
        print("\nCleaning orders...")
        orig = len(df)
        df = df.drop_duplicates()
        
        missing = df['shipping_cost'].isna().sum()
        if missing > 0:
            median_cost = df['shipping_cost'].median()
            df['shipping_cost'] = df['shipping_cost'].fillna(median_cost)
            print(f"  Filled {missing} missing shipping costs")
        
        df['order_month'] = df['order_date'].dt.to_period('M')
        df['order_year'] = df['order_date'].dt.year
        df['order_quarter'] = df['order_date'].dt.quarter
        df['day_of_week'] = df['order_date'].dt.day_name()
        df['total_order_value'] = df['total_amount'] + df['shipping_cost']
        
        df = df[df['total_order_value'] > 0]
        
        print(f"  Removed {orig - len(df)} invalid records -> {len(df)} records")
        return df
    
    def create_fact_sales(self, orders, products, customers):
        print("\nBuilding fact table...")
        
        fact = orders.merge(
            products[['product_id', 'category', 'cost', 'profit_margin', 'price_tier']],
            on='product_id',
            how='left'
        ).merge(
            customers[['customer_id', 'customer_segment', 'country']],
            on='customer_id',
            how='left'
        )
        
        fact['revenue'] = fact['total_amount']
        fact['cost_of_goods'] = fact['cost'] * fact['quantity']
        fact['gross_profit'] = fact['revenue'] - fact['cost_of_goods']
        
        completed = fact[fact['status'] == 'Completed']
        total_rev = completed['revenue'].sum()
        total_profit = completed['gross_profit'].sum()
        
        print(f"  Created {len(fact)} sales records")
        print(f"  Total revenue: ${total_rev:,.2f}")
        print(f"  Total profit: ${total_profit:,.2f}")
        
        return fact
    
    def transform_all(self, data):
        print("\n--- TRANSFORM ---")
        
        customers = self.clean_customers(data['customers'])
        products = self.clean_products(data['products'])
        orders = self.clean_orders(data['orders'])
        fact_sales = self.create_fact_sales(orders, products, customers)
        
        return {
            'customers': customers,
            'products': products,
            'orders': orders,
            'fact_sales': fact_sales
        }

if __name__ == "__main__":
    from extract import DataExtractor
    
    extractor = DataExtractor()
    raw = extractor.extract_all()
    
    transformer = DataTransformer()
    clean = transformer.transform_all(raw)
