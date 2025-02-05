from scripts.constants import REDSHIFT_SCHEMA
from scripts.connections import get_redshift_conn

def generate_reports():
    redshift_hook = get_redshift_conn()
    
    # Report 1: Daily Sales Performance
    daily_sales_query = f"""
        SELECT 
            SUM(total_amount) AS total_revenue,
            COUNT(order_id) AS total_orders,
            AVG(total_amount) AS avg_order_value
        FROM {REDSHIFT_SCHEMA}.sales
        WHERE sale_date = CURRENT_DATE;
    """
    daily_sales_report = redshift_hook.get_records(daily_sales_query)
    
    # Report 2: Top-Selling Products
    top_products_query = f"""
        SELECT 
            p.name AS product_name,
            SUM(o.quantity) AS total_quantity_sold,
            SUM(s.total_amount) AS total_revenue
        FROM {REDSHIFT_SCHEMA}.orders o
        JOIN {REDSHIFT_SCHEMA}.products p ON o.product_id = p.product_id
        JOIN {REDSHIFT_SCHEMA}.sales s ON o.order_id = s.order_id
        WHERE s.sale_date = CURRENT_DATE
        GROUP BY p.name
        ORDER BY total_revenue DESC
        LIMIT 10;
    """
    top_products_report = redshift_hook.get_records(top_products_query)
    
    # Add similar queries for other reports...
    
    return {
        "daily_sales_report": daily_sales_report,
        "top_products_report": top_products_report,
        "abc" : [],
        # Add other reports here...
    }