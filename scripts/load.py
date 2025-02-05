from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from scripts.constants import REDSHIFT_SCHEMA, S3_BUCKET

def create_load_task(dag, table_name):
    return S3ToRedshiftOperator(
        task_id=f"load_{table_name}",
        schema=REDSHIFT_SCHEMA,
        table=table_name,
        s3_bucket=S3_BUCKET,
        s3_key=f"transformed/{table_name}.csv",
        redshift_conn_id="redshift_default",
        aws_conn_id="aws_default",
        copy_options=["CSV", "IGNOREHEADER 1"],
        dag=dag,
    )