import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

class DataVisualizer:
    def __init__(self, db_path='output/ecommerce.db'):
        self.db_path = db_path
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_data(self, query):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def monthly_revenue_chart(self):
        query = """
            SELECT order_month, SUM(revenue) as total_revenue, SUM(gross_profit) as total_profit
            FROM fact_sales
            WHERE status = 'Completed'
            GROUP BY order_month
            ORDER BY order_month
        """
        df = self.load_data(query)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['order_month'], y=df['total_revenue'], 
                                 mode='lines+markers', name='Revenue', line=dict(width=3)))
        fig.add_trace(go.Scatter(x=df['order_month'], y=df['total_profit'], 
                                 mode='lines+markers', name='Profit', line=dict(width=3)))
        
        fig.update_layout(title='Monthly Revenue & Profit Trend', 
                         xaxis_title='Month', yaxis_title='Amount ($)',
                         hovermode='x unified', height=500)
        
        fig.write_html(f'{self.output_dir}/monthly_revenue.html')
        print("  Created monthly_revenue.html")
    
    def category_performance_chart(self):
        query = """
            SELECT category, 
                   SUM(revenue) as total_revenue,
                   SUM(gross_profit) as total_profit,
                   COUNT(*) as order_count
            FROM fact_sales
            WHERE status = 'Completed'
            GROUP BY category
            ORDER BY total_revenue DESC
        """
        df = self.load_data(query)
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Revenue by Category', 'Profit by Category'))
        
        fig.add_trace(go.Bar(x=df['category'], y=df['total_revenue'], name='Revenue',
                            marker_color='lightblue'), row=1, col=1)
        fig.add_trace(go.Bar(x=df['category'], y=df['total_profit'], name='Profit',
                            marker_color='lightgreen'), row=1, col=2)
        
        fig.update_layout(height=500, showlegend=False, title_text="Category Performance Analysis")
        fig.write_html(f'{self.output_dir}/category_performance.html')
        print("  Created category_performance.html")
    
    def customer_segment_chart(self):
        query = """
            SELECT customer_segment, 
                   SUM(revenue) as total_revenue,
                   COUNT(DISTINCT customer_id) as customer_count
            FROM fact_sales
            WHERE status = 'Completed'
            GROUP BY customer_segment
        """
        df = self.load_data(query)
        
        fig = go.Figure(data=[go.Pie(labels=df['customer_segment'], 
                                     values=df['total_revenue'],
                                     hole=.3)])
        fig.update_layout(title='Revenue by Customer Segment', height=500)
        fig.write_html(f'{self.output_dir}/customer_segments.html')
        print("  Created customer_segments.html")
    
    def top_products_chart(self):
        query = """
            SELECT p.product_name, p.category,
                   SUM(f.revenue) as total_revenue,
                   SUM(f.quantity) as units_sold
            FROM fact_sales f
            JOIN dim_products p ON f.product_id = p.product_id
            WHERE f.status = 'Completed'
            GROUP BY p.product_id
            ORDER BY total_revenue DESC
            LIMIT 10
        """
        df = self.load_data(query)
        
        fig = go.Figure(go.Bar(
            x=df['total_revenue'],
            y=df['product_name'],
            orientation='h',
            marker_color='coral'
        ))
        fig.update_layout(title='Top 10 Products by Revenue', 
                         xaxis_title='Revenue ($)', yaxis_title='Product',
                         height=500)
        fig.write_html(f'{self.output_dir}/top_products.html')
        print("  Created top_products.html")
    
    def country_analysis_chart(self):
        query = """
            SELECT country, 
                   SUM(revenue) as total_revenue,
                   COUNT(*) as order_count,
                   AVG(revenue) as avg_order_value
            FROM fact_sales
            WHERE status = 'Completed'
            GROUP BY country
            ORDER BY total_revenue DESC
        """
        df = self.load_data(query)
        
        fig = px.bar(df, x='country', y='total_revenue', 
                    title='Revenue by Country',
                    labels={'total_revenue': 'Total Revenue ($)', 'country': 'Country'})
        fig.write_html(f'{self.output_dir}/country_analysis.html')
        print("  Created country_analysis.html")
    
    def generate_summary_stats(self):
        query = """
            SELECT 
                COUNT(DISTINCT customer_id) as total_customers,
                COUNT(DISTINCT product_id) as total_products,
                COUNT(*) as total_orders,
                SUM(revenue) as total_revenue,
                SUM(gross_profit) as total_profit,
                AVG(revenue) as avg_order_value,
                AVG(gross_profit) / AVG(revenue) * 100 as avg_profit_margin
            FROM fact_sales
            WHERE status = 'Completed'
        """
        df = self.load_data(query)
        
        stats_html = f"""
        <html>
        <head><title>Summary Statistics</title></head>
        <body style='font-family: Arial; padding: 20px;'>
            <h1>E-Commerce Analytics Summary</h1>
            <table style='border-collapse: collapse; width: 100%;'>
                <tr style='background: #f0f0f0;'>
                    <th style='border: 1px solid #ddd; padding: 12px; text-align: left;'>Metric</th>
                    <th style='border: 1px solid #ddd; padding: 12px; text-align: right;'>Value</th>
                </tr>
                <tr><td style='border: 1px solid #ddd; padding: 12px;'>Total Customers</td>
                    <td style='border: 1px solid #ddd; padding: 12px; text-align: right;'>{df['total_customers'].iloc[0]:,}</td></tr>
                <tr><td style='border: 1px solid #ddd; padding: 12px;'>Total Products</td>
                    <td style='border: 1px solid #ddd; padding: 12px; text-align: right;'>{df['total_products'].iloc[0]:,}</td></tr>
                <tr><td style='border: 1px solid #ddd; padding: 12px;'>Total Orders</td>
                    <td style='border: 1px solid #ddd; padding: 12px; text-align: right;'>{df['total_orders'].iloc[0]:,}</td></tr>
                <tr><td style='border: 1px solid #ddd; padding: 12px;'>Total Revenue</td>
                    <td style='border: 1px solid #ddd; padding: 12px; text-align: right;'>${df['total_revenue'].iloc[0]:,.2f}</td></tr>
                <tr><td style='border: 1px solid #ddd; padding: 12px;'>Total Profit</td>
                    <td style='border: 1px solid #ddd; padding: 12px; text-align: right;'>${df['total_profit'].iloc[0]:,.2f}</td></tr>
                <tr><td style='border: 1px solid #ddd; padding: 12px;'>Avg Order Value</td>
                    <td style='border: 1px solid #ddd; padding: 12px; text-align: right;'>${df['avg_order_value'].iloc[0]:,.2f}</td></tr>
                <tr><td style='border: 1px solid #ddd; padding: 12px;'>Avg Profit Margin</td>
                    <td style='border: 1px solid #ddd; padding: 12px; text-align: right;'>{df['avg_profit_margin'].iloc[0]:.1f}%</td></tr>
            </table>
        </body>
        </html>
        """
        
        with open(f'{self.output_dir}/summary_stats.html', 'w') as f:
            f.write(stats_html)
        print("  Created summary_stats.html")
    
    def run_all(self):
        print("\n--- VISUALIZE ---")
        print("\nGenerating visualizations...")
        
        self.monthly_revenue_chart()
        self.category_performance_chart()
        self.customer_segment_chart()
        self.top_products_chart()
        self.country_analysis_chart()
        self.generate_summary_stats()
        
        print(f"\nAll visualizations saved to '{self.output_dir}/' directory")

if __name__ == "__main__":
    visualizer = DataVisualizer()
    visualizer.run_all()
