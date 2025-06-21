#!/bin/bash

# Wait for the DB to be ready
sleep 10

# Initialize and create user if not already created
airflow db init

airflow users create \
  --username admin \
  --firstname Segun \
  --lastname Admin \
  --role Admin \
  --email admin@example.com \
  --password admin

# Start Airflow webserver
exec airflow webserver
