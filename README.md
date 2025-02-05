## **Project Overview**
This project implements a **data pipeline** using **Apache Airflow** to extract data from a **PostgreSQL database**, transform it, and load it into **Amazon Redshift** for analytics and reporting. The pipeline ensures **daily updates** to meet the Marketing team's requirements. Key features include:
- **ETL Pipeline**: Extract, Transform, Load (ETL) workflow orchestrated by Airflow.
- **Data Transformation**: Handling JSON data, resolving null values, and normalizing schemas.
- **Data Governance**: Implementing PII anonymization and role-based access control.
- **Performance Optimization**: Partitioning, indexing, and clustering for large-scale data.

---

## **Directory Structure**
```
root/
├── dags/
│   └── etl_pipeline.py            # Main Airflow DAG for the ETL pipeline
├── scripts/
│   ├── connections.py             # Connection configurations for PostgreSQL, S3, and Redshift
│   ├── constants.py               # Constants like table names and S3 bucket
│   ├── extract.py                 # Functions to extract data from PostgreSQL to S3
│   ├── transform.py               # Functions to transform data (e.g., JSON normalization)
│   ├── load.py                    # Functions to load data from S3 to Redshift
│   └── reports.py                 # Functions to generate reports from Redshift
├── docker-compose.yml             # Docker Compose file for Airflow setup
├── entrypoint.sh                  # Entrypoint script for Airflow containers
├── requirements.txt               # Python dependencies for the project
├── README.md                      # This file
```

---

## **File Descriptions**

### **1. `dags/etl_pipeline.py`**
- **Description**: The main Airflow DAG that orchestrates the ETL pipeline.
- **Tasks**:
  - **Extract**: Extract data from PostgreSQL and upload to S3.
  - **Transform**: Clean and transform data (e.g., handle null values, normalize JSON).
  - **Load**: Load transformed data into Redshift.
  - **Generate Reports**: Generate daily reports using SQL queries in Redshift.

### **2. `scripts/connections.py`**
- **Description**: Contains connection configurations for PostgreSQL, S3, and Redshift.
- **Functions**:
  - `get_postgres_conn()`: Returns a PostgreSQL connection.
  - `get_s3_conn()`: Returns an S3 connection.
  - `get_redshift_conn()`: Returns a Redshift connection.

### **3. `scripts/constants.py`**
- **Description**: Stores constants like table names, S3 bucket, and Redshift schema.
- **Example**:
  ```python
  POSTGRES_TABLES = ["customers", "products", "orders", "sales"]
  S3_BUCKET = "your-s3-bucket-name"
  REDSHIFT_SCHEMA = "public"
  ```

### **4. `scripts/extract.py`**
- **Description**: Contains functions to extract data from PostgreSQL and upload it to S3.
- **Functions**:
  - `extract_table_to_s3(table_name)`: Extracts data from a PostgreSQL table and uploads it to S3.

### **5. `scripts/transform.py`**
- **Description**: Contains functions to transform data (e.g., handle null values, normalize JSON).
- **Functions**:
  - `transform_orders(s3_key)`: Handles null values in the `quantity` column.
  - `transform_customers(s3_key)`: Normalizes the JSON `address` field.

### **6. `scripts/load.py`**
- **Description**: Contains functions to load data from S3 into Redshift.
- **Functions**:
  - `create_load_task(dag, table_name)`: Creates an Airflow task to load data into Redshift.

### **7. `scripts/reports.py`**
- **Description**: Contains functions to generate reports from Redshift.
- **Functions**:
  - `generate_reports()`: Generates daily reports using SQL queries.

### **8. `docker-compose.yml`**
- **Description**: Docker Compose file to set up Airflow, PostgreSQL, and other services.
- **Services**:
  - `postgres`: PostgreSQL database for Airflow metadata.
  - `airflow-webserver`: Airflow webserver UI.
  - `airflow-scheduler`: Airflow scheduler to run DAGs.

### **9. `entrypoint.sh`**
- **Description**: Entrypoint script for Airflow containers. Initializes the Airflow database and installs dependencies.

### **10. `requirements.txt`**
- **Description**: Lists Python dependencies for the project.
- **Example**:
  ```
  apache-airflow-providers-postgres
  apache-airflow-providers-amazon
  pandas
  ```

---

## **How to Run the Project Using Docker**

### **Prerequisites**
1. Install **Docker** and **Docker Compose**.
2. Ensure ports `8080` (Airflow UI) and `5432` (PostgreSQL) are available.

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-airflow-project.git
   cd your-airflow-project
   ```
2. Build and start the Docker containers:
   ```bash
   docker-compose up
   ```
3. Access the Airflow UI:
   - Open `http://localhost:8080` in your browser.
   - Use `admin` as the username and password.
4. Trigger the `etl_pipeline` DAG:
   - In the Airflow UI, find the `etl_pipeline` DAG and click the **Trigger DAG** button.

---

## **Main DAG and ETL Pipeline**

### **DAG Overview**
- **DAG Name**: `etl_pipeline`
- **Schedule**: Daily (`@daily`)
- **Tasks**:
  1. **Extract**: Extract data from PostgreSQL and upload to S3.
  2. **Transform**: Clean and transform data (e.g., handle null values, normalize JSON).
  3. **Load**: Load transformed data into Redshift.
  4. **Generate Reports**: Generate daily reports using SQL queries in Redshift.

### **Task Dependencies**
```
extract_tasks >> [transform_orders_task, transform_customers_task] >> load_tasks >> generate_reports_task
```

---

## **Assumptions**
1. **Data Volume**: The dataset is small enough for daily batch processing.
2. **Data Freshness**: The Marketing team requires data by the end of each day.
3. **Tools**: Apache Airflow, Amazon S3, and Redshift are available and properly configured.
4. **Future Reports**: Additional reports (e.g., customer lifetime value) will be implemented later.

---

## **Design Decisions**
1. **Modularity**: Each script (`extract.py`, `transform.py`, `load.py`, `reports.py`) has a single responsibility.
2. **Scalability**: The pipeline is designed to handle increasing data volumes.
3. **Best Practices**: Uses Airflow’s built-in operators and hooks for efficiency and maintainability.


