#!/bin/bash

# Wait for the DB to be ready
sleep 10

# Initialize and create user if not already created
airflow db migrate

airflow users sync

# Start Airflow webserver
exec airflow api-server
