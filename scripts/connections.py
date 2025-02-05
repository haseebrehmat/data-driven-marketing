from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.contrib.hooks.redshift_hook import RedshiftHook

# PostgreSQL Connection
def get_postgres_conn():
    return PostgresHook(postgres_conn_id="postgres_default").get_conn()

# S3 Connection
def get_s3_conn():
    return S3Hook(aws_conn_id="aws_default").get_conn()

# Redshift Connection
def get_redshift_conn():
    return RedshiftHook(redshift_conn_id="redshift_default").get_conn()