import pandas as pd
from scripts.connections import get_postgres_conn, get_s3_conn
from scripts.constants import S3_BUCKET
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def extract_table_to_s3(table_name):
    # Extract data from PostgreSQL
    conn = get_postgres_conn()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    
    # Upload to S3
    s3_conn = get_s3_conn()
    s3_key = f"raw/{table_name}.csv"
    s3_conn.load_string(
        string_data=df.to_csv(index=False),
        key=s3_key,
        bucket_name=S3_BUCKET,
        replace=True
    )
    return s3_key