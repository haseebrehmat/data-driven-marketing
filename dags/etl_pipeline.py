# dags/etl_pipeline.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.extract import extract_table_to_s3
from scripts.transform import transform_orders, transform_customers
from scripts.load import create_load_task
from scripts.reports import generate_reports
from scripts.constants import POSTGRES_TABLES

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 10, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

# Extract Tasks
extract_tasks = []
for table in POSTGRES_TABLES:
    task = PythonOperator(
        task_id=f"extract_{table}",
        python_callable=extract_table_to_s3,
        op_kwargs={"table_name": table},
        dag=dag,
    )
    extract_tasks.append(task)

# Transform Tasks
transform_orders_task = PythonOperator(
    task_id="transform_orders",
    python_callable=transform_orders,
    op_kwargs={"s3_key": "raw/orders.csv"},
    dag=dag,
)

transform_customers_task = PythonOperator(
    task_id="transform_customers",
    python_callable=transform_customers,
    op_kwargs={"s3_key": "raw/customers.csv"},
    dag=dag,
)

# Load Tasks
load_tasks = []
for table in POSTGRES_TABLES:
    task = PythonOperator(
        task_id=f"load_{table}",
        python_callable=create_load_task,
        op_kwargs={"table_name": table, "s3_key": f"transformed/{table}.csv"},
        dag=dag,
    )
    load_tasks.append(task)

# Report Generation Task
generate_reports_task = PythonOperator(
    task_id="generate_reports",
    python_callable=generate_reports,
    dag=dag,
)

# Define Task Dependencies
# Define Task Dependencies
# Extract tasks run in parallel
for extract_task in extract_tasks:
    extract_task >> [transform_orders_task, transform_customers_task]

# Transform tasks run in parallel
transform_orders_task >> load_tasks
transform_customers_task >> load_tasks

# Load tasks run in parallel
for load_task in load_tasks:
    load_task >> generate_reports_task