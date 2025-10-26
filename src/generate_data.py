import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_ORDERS = 2000

def generate_customers(n):
    start_date = datetime(2024, 1, 1)
    customers = pd.DataFrame({
        'customer_id': range(1, n + 1),
        'customer_name': [f'Customer_{i}' for i in range(1, n + 1)],
        'email': [f'customer{i}@email.com' for i in range(1, n + 1)],
        'registration_date': [start_date + timedelta(days=random.randint(0, 300)) for _ in range(n)],
        'country': np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France'], n, p=[0.4, 0.2, 0.15, 0.15, 0.1]),
        'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic'], n, p=[0.2, 0.5, 0.3])
    })
    return customers

def generate_products(n):
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
    products = pd.DataFrame({
        'product_id': range(1, n + 1),
        'product_name': [f'Product_{i}' for i in range(1, n + 1)],
        'category': np.random.choice(categories, n),
        'base_price': np.random.uniform(10, 500, n).round(2),
        'cost': np.random.uniform(5, 250, n).round(2)
    })
    return products

def generate_orders(num_orders, customers, products):
    orders = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 10, 31)
    days = (end_date - start_date).days
    
    for order_id in range(1, num_orders + 1):
        customer_id = random.randint(1, len(customers))
        order_date = start_date + timedelta(days=random.randint(0, days))
        num_items = random.randint(1, 5)
        
        for item in range(num_items):
            product_id = random.randint(1, len(products))
            product = products[products['product_id'] == product_id].iloc[0]
            quantity = random.randint(1, 3)
            price = product['base_price'] * random.uniform(0.9, 1.1)
            status = np.random.choice(['Completed', 'Pending', 'Cancelled', 'Returned'], p=[0.85, 0.05, 0.05, 0.05])
            
            orders.append({
                'order_id': order_id,
                'customer_id': customer_id,
                'product_id': product_id,
                'order_date': order_date,
                'quantity': quantity,
                'unit_price': round(price, 2),
                'total_amount': round(price * quantity, 2),
                'status': status,
                'shipping_cost': round(random.uniform(5, 25), 2) if item == 0 else 0
            })
    
    return pd.DataFrame(orders)

if __name__ == '__main__':
    print("Generating data...")
    
    customers = generate_customers(NUM_CUSTOMERS)
    products = generate_products(NUM_PRODUCTS)
    orders = generate_orders(NUM_ORDERS, customers, products)
    
    orders.loc[random.sample(range(len(orders)), 20), 'shipping_cost'] = np.nan
    duplicate_orders = orders.sample(10)
    orders = pd.concat([orders, duplicate_orders], ignore_index=True)
    
    customers.to_csv('data/customers.csv', index=False)
    products.to_csv('data/products.csv', index=False)
    orders.to_csv('data/orders.csv', index=False)
    
    print(f"Created {len(customers)} customers, {len(products)} products, {len(orders)} orders")
