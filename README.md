# Weather Data Pipeline with Apache Airflow

A containerized weather data collection and processing pipeline using Apache Airflow, PostgreSQL, and the WeatherStack API. This project automatically fetches weather data for Leipzig, Germany and stores it in a PostgreSQL database for analysis and monitoring.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   WeatherStack  │    │    Apache        │    │    PostgreSQL       │
│      API        │───▶│    Airflow       │───▶│    Databases        │
│                 │    │                  │    │                     │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                              │                         │
                              │                         ├─ weather_db
                              │                         └─ airflow_db
                              ▼
                       ┌──────────────────┐
                       │    PgAdmin       │
                       │   (Web UI)       │
                       └──────────────────┘
```

## Features

- **Automated Weather Data Collection**: Fetches current weather data from WeatherStack API
- **Comprehensive Data Storage**: Stores weather conditions, air quality, astronomical data
- **Containerized Architecture**: Full Docker setup with Docker Compose
- **Database Management**: Separate databases for weather data and Airflow metadata
- **Web Interface**: PgAdmin for database management and Airflow for pipeline monitoring
- **Error Handling**: Robust error handling and logging throughout the pipeline

## Prerequisites

- Docker and Docker Compose installed
- WeatherStack API key (free tier available at [weatherstack.com](https://weatherstack.com))
- At least 2GB of available RAM for containers

## Project Structure

```
weather-pipeline/
├── docker-compose.yml          # Multi-container Docker application
├── Dockerfile                  # Custom Airflow image
├── requirements.txt            # Python dependencies
├── entrypoint.sh              # Airflow initialization script
├── .env                       # Environment variables
├── weather_data_collector.py  # Main weather data collection script
├── dags/                      # Airflow DAGs directory
├── logs/                      # Airflow logs
├── plugins/                   # Airflow plugins
├── weather_postgres_data/     # Weather database volume
└── airflow_postgres_data/     # Airflow database volume
```

## 🔧 Setup Instructions

### 1. Clone and Configure

```bash
git clone <your-repo-url>
cd weather-pipeline
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Weather API Configuration
WEATHER_API_KEY=your_weatherstack_api_key_here

# Airflow Configuration
AIRFLOW_IMAGE=apache/airflow:3.0.0
AIRFLOW_EXECUTOR=LocalExecutor
AIRFLOW_CONN=postgresql+psycopg2://airflow:airflow@airflow_db:5432/airflow_db
AIRFLOW_WEBSERVER_WORKERS=4
AIRFLOW_PORT=8080

# Airflow System Configuration
AIRFLOW_HOME=/opt/airflow
AIRFLOW_UID=50000
```

### 3. Create Required Directories

```bash
mkdir -p dags logs plugins weather_postgres_data airflow_postgres_data
```

### 4. Set Permissions

```bash
# Set proper ownership for Airflow directories
sudo chown -R 50000:50000 dags logs plugins
```

### 5. Build and Start Services

```bash
# Build and start all containers
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

## Access Points

Once the containers are running:

- **Airflow Web UI**: http://localhost:8000
- **PgAdmin**: http://localhost:8080
  - Email: `admin@admin.com`
  - Password: `root`

## Database Schema

The weather data is stored in the `weather_data` table with the following key columns:

### Location Information
- `city`, `country`, `region`
- `localtime` (timestamp)

### Weather Conditions
- `temperature`, `feels_like`
- `weather_description`, `weather_icon`
- `humidity`, `cloudcover`, `visibility`
- `uv_index`, `is_day`

### Wind Information
- `wind_speed`, `wind_degree`, `wind_dir`
- `pressure`, `precip`

### Astronomical Data
- `sunrise`, `sunset`
- `moonrise`, `moonset`, `moon_phase`, `moon_illumination`

### Air Quality
- `air_quality_co`, `air_quality_no2`, `air_quality_o3`
- `air_quality_so2`, `air_quality_pm2_5`, `air_quality_pm10`
- `us_epa_index`, `gb_defra_index`

## Usage Examples

### Running the Weather Data Collector Manually

```bash
# Inside the Airflow container
docker exec -it airflow_container python /opt/airflow/weather_data_collector.py
```

### Connecting to Databases

**Weather Database:**
```
Host: localhost
Port: 5432
Database: weather_db
Username: root
Password: root
```

**Airflow Database:**
```
Host: localhost
Port: 5433
Database: airflow_db
Username: airflow
Password: airflow
```

### Sample SQL Queries

```sql
-- Get latest weather data
SELECT * FROM weather_data ORDER BY localtime DESC LIMIT 1;

-- Average temperature over time
SELECT DATE(localtime), AVG(temperature) as avg_temp 
FROM weather_data 
GROUP BY DATE(localtime) 
ORDER BY DATE(localtime);

-- Air quality trends
SELECT localtime, air_quality_pm2_5, air_quality_pm10 
FROM weather_data 
WHERE air_quality_pm2_5 IS NOT NULL 
ORDER BY localtime DESC;
```

## Error Handling

The pipeline includes comprehensive error handling:

- **API Failures**: Graceful handling of WeatherStack API errors
- **Database Connectivity**: Automatic retry logic for database connections
- **Data Validation**: Validation of API responses before database insertion
- **Logging**: Detailed logging for troubleshooting

## Monitoring and Maintenance

### Logs Location
- **Airflow Logs**: `./logs/` directory
- **Container Logs**: `docker-compose logs [service-name]`

### Health Checks
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs airflow
docker-compose logs pgdatabase

# Access container shell
docker exec -it airflow_container bash
```

## Development

### Adding New DAGs
1. Place DAG files in the `./dags/` directory
2. Airflow will automatically detect and load them

### Modifying Dependencies
1. Update `requirements.txt`
2. Rebuild the container: `docker-compose up --build`

### Database Migrations
The application automatically creates the required table structure on first run.

## Troubleshooting

### Common Issues

**Container fails to start:**
```bash
# Check container logs
docker-compose logs [service-name]

# Rebuild containers
docker-compose down
docker-compose up --build
```

**Database connection issues:**
```bash
# Verify database is running
docker-compose ps pgdatabase

# Check network connectivity
docker exec -it airflow_container ping pgdatabase
```

**Permission errors:**
```bash
# Fix Airflow directory permissions
sudo chown -R 50000:50000 dags logs plugins
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [WeatherStack](https://weatherstack.com) for the weather API
- [Apache Airflow](https://airflow.apache.org) for workflow orchestration
- [PostgreSQL](https://www.postgresql.org) for data storage