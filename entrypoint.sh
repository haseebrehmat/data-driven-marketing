#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install custom requirements if requirements.txt exists
if [ -f "/opt/airflow/requirements.txt" ]; then
    pip install --no-cache-dir -r /opt/airflow/requirements.txt
fi

# Initialize Airflow database if it hasn't been initialized
if [ ! -f "/opt/airflow/airflow-webserver.pid" ]; then
    airflow db init
    
    # Create default admin user if running webserver
    if [ "$1" = "webserver" ]; then
        airflow users create \
            --username admin \
            --password admin \
            --firstname Anonymous \
            --lastname Admin \
            --role Admin \
            --email admin@example.com
    fi
fi

# Start the requested service
case "$1" in
  webserver)
    exec airflow webserver
    ;;
  scheduler)
    exec airflow scheduler
    ;;
  *)
    exec "$@"
    ;;
esac