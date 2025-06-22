# Use official Apache Airflow base image
FROM apache/airflow:3.0.0

# Set build arguments
ARG AIRFLOW_UID=${AIRFLOW_UID}

# Set environment variables
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Set working directory
WORKDIR $AIRFLOW_HOME

# Switch to root user for system-level operations
USER root

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy entrypoint script and set permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch back to Airflow user for security
USER $AIRFLOW_UID
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

USER root
# Set appropriate permissions for Airflow directories
RUN chown -R $AIRFLOW_UID:$AIRFLOW_UID /opt/airflow


# Set entrypoint and default command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["airflow", "scheduler"]

USER airflow