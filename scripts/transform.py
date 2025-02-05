import pandas as pd
from scripts.connections import get_s3_conn
from scripts.constants import S3_BUCKET

def transform_orders(s3_key):
    # Download from S3
    s3_conn = get_s3_conn()
    obj = s3_conn.get_key(key=s3_key, bucket_name=S3_BUCKET)
    df = pd.read_csv(obj.get()["Body"])
    
    # Handle null values in 'quantity'
    df["quantity"].fillna(0, inplace=True)
    
    # Upload transformed data back to S3
    transformed_key = s3_key.replace("raw", "transformed")
    s3_conn.load_string(
        string_data=df.to_csv(index=False),
        key=transformed_key,
        bucket_name=S3_BUCKET,
        replace=True
    )
    return transformed_key

def transform_customers(s3_key):
    # Download from S3
    s3_conn = get_s3_conn()
    obj = s3_conn.get_key(key=s3_key, bucket_name=S3_BUCKET)
    df = pd.read_csv(obj.get()["Body"])
    
    # Normalize JSON 'address' field
    df = pd.concat([df.drop(["address"], axis=1), df["address"].apply(pd.Series)], axis=1)
    
    # Upload transformed data back to S3
    transformed_key = s3_key.replace("raw", "transformed")
    s3_conn.load_string(
        string_data=df.to_csv(index=False),
        key=transformed_key,
        bucket_name=S3_BUCKET,
        replace=True
    )
    return transformed_key