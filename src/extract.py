import pandas as pd
import os

class DataExtractor:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        
    def extract_customers(self):
        path = os.path.join(self.data_dir, 'customers.csv')
        df = pd.read_csv(path)
        print(f"Extracted {len(df)} customers")
        return df
    
    def extract_products(self):
        path = os.path.join(self.data_dir, 'products.csv')
        df = pd.read_csv(path)
        print(f"Extracted {len(df)} products")
        return df
    
    def extract_orders(self):
        path = os.path.join(self.data_dir, 'orders.csv')
        df = pd.read_csv(path, parse_dates=['order_date'])
        print(f"Extracted {len(df)} orders")
        return df
    
    def extract_all(self):
        print("\n--- EXTRACT ---")
        return {
            'customers': self.extract_customers(),
            'products': self.extract_products(),
            'orders': self.extract_orders()
        }

if __name__ == "__main__":
    extractor = DataExtractor()
    data = extractor.extract_all()
