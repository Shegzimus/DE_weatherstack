import os
import requests
from dotenv import load_dotenv
from typing import Optional

from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Configuration
city: str = "Leipzig"
key: str = os.getenv("WEATHER_API_KEY")

# Database connection
engine = create_engine("postgresql://root:root@localhost:5432/weather_db")


def fetch_api_data(api_url: str, headers=None) -> Optional[dict]:
    """
    Fetch data from a given API URL.

    :param api_url: The URL of the API endpoint.
    :param headers: Optional headers to include in the request.
    :return: The JSON response from the API or None if an error occurs.
    """
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
        return None


def connect_to_db():
    """
    Connect to the PostgreSQL database.
    """
    try:
        connection = engine.connect()
        print("Database connection successful.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def create_table():
    """
    Create a table in the PostgreSQL database if it does not exist.
    """
    connection = connect_to_db()
    if connection:
        try:
            with connection.begin():
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS weather_data (
                        id SERIAL PRIMARY KEY,
                        city TEXT,
                        country TEXT,
                        region TEXT,
                        "localtime" TIMESTAMP,
                        temperature FLOAT,
                        feels_like FLOAT,
                        weather_description TEXT,
                        weather_icon TEXT,
                        wind_speed FLOAT,
                        wind_degree INTEGER,
                        wind_dir TEXT,
                        pressure INTEGER,
                        precip FLOAT,
                        humidity INTEGER,
                        cloudcover INTEGER,
                        uv_index INTEGER,
                        visibility FLOAT,
                        is_day BOOLEAN,
                        sunrise TIME,
                        sunset TIME,
                        moonrise TIME,
                        moonset TIME,
                        moon_phase TEXT,
                        moon_illumination INTEGER,
                        air_quality_co FLOAT,
                        air_quality_no2 FLOAT,
                        air_quality_o3 FLOAT,
                        air_quality_so2 FLOAT,
                        air_quality_pm2_5 FLOAT,
                        air_quality_pm10 FLOAT,
                        us_epa_index INTEGER,
                        gb_defra_index INTEGER
                    )
                """))
            print("Table created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            connection.close()


def insert_records(conn, data):
    """
    Insert weather data records into the database.
    
    :param conn: SQLAlchemy connection object
    :param data: Weather data dictionary from API
    """
    print("Inserting records into the database...")

    try:
        weather_data = data.get("current", {})
        location_data = data.get("location", {})
        
        # Use SQLAlchemy's text() for parameterized queries
        insert_query = text("""
            INSERT INTO weather_data (
                city, country, region, "localtime", temperature, feels_like,
                weather_description, weather_icon, wind_speed, wind_degree,
                wind_dir, pressure, precip, humidity, cloudcover,
                uv_index, visibility, is_day, sunrise, sunset,
                moonrise, moonset, moon_phase, moon_illumination,
                air_quality_co, air_quality_no2, air_quality_o3,
                air_quality_so2, air_quality_pm2_5, air_quality_pm10,
                us_epa_index, gb_defra_index
            ) VALUES (
                :city, :country, :region, :localtime, :temperature,
                :feels_like, :weather_description, :weather_icon,
                :wind_speed, :wind_degree, :wind_dir, :pressure,
                :precip, :humidity, :cloudcover, :uv_index,
                :visibility, :is_day, :sunrise, :sunset,
                :moonrise, :moonset, :moon_phase,
                :moon_illumination, :air_quality_co,
                :air_quality_no2, :air_quality_o3,
                :air_quality_so2, :air_quality_pm2_5,
                :air_quality_pm10, :us_epa_index,
                :gb_defra_index
            )
        """)
        
        # Prepare data for insertion
        insert_data = {
            "city": location_data.get("name"),
            "country": location_data.get("country"),
            "region": location_data.get("region"),
            "localtime": location_data.get("localtime"),
            "temperature": weather_data.get("temperature"),
            "feels_like": weather_data.get("feelslike"),
            "weather_description": weather_data.get("weather_descriptions", [])[0] if weather_data.get("weather_descriptions") else None,
            "weather_icon": weather_data.get("weather_icons", [])[0] if weather_data.get("weather_icons") else None,
            "wind_speed": weather_data.get("wind_speed"),
            "wind_degree": weather_data.get("wind_degree"),
            "wind_dir": weather_data.get("wind_dir"),
            "pressure": weather_data.get("pressure"),
            "precip": weather_data.get("precip"),
            "humidity": weather_data.get("humidity"),
            "cloudcover": weather_data.get("cloudcover"),
            "uv_index": weather_data.get("uv_index"),
            "visibility": weather_data.get("visibility"),
            "is_day": weather_data.get("is_day") == 'yes',
            "sunrise": location_data.get("sunrise"),
            "sunset": location_data.get("sunset"),
            "moonrise": location_data.get("moonrise"),
            "moonset": location_data.get("moonset"),
            "moon_phase": location_data.get("moon_phase"),
            "moon_illumination": location_data.get("moon_illumination"),
            "air_quality_co": weather_data.get("air_quality", {}).get("co") if weather_data.get("air_quality") else None,
            "air_quality_no2": weather_data.get("air_quality", {}).get("no2") if weather_data.get("air_quality") else None,
            "air_quality_o3": weather_data.get("air_quality", {}).get("o3") if weather_data.get("air_quality") else None,
            "air_quality_so2": weather_data.get("air_quality", {}).get("so2") if weather_data.get("air_quality") else None,
            "air_quality_pm2_5": weather_data.get("air_quality", {}).get("pm2_5") if weather_data.get("air_quality") else None,
            "air_quality_pm10": weather_data.get("air_quality", {}).get("pm10") if weather_data.get("air_quality") else None,
            "us_epa_index": weather_data.get("us_epa_index"),
            "gb_defra_index": weather_data.get("gb_defra_index")
        }
        
        # Execute the insert within a transaction
        with conn.begin():
            conn.execute(insert_query, insert_data)
        
        print("Records inserted successfully.")
        
    except Exception as e:
        print(f"Error inserting records: {e}")
        raise


def main():
    """
    Main function to execute the API request and insert data into database.
    """
    # Validate API key
    if not key:
        print("Error: WEATHER_API_KEY not found in environment variables.")
        return

    # Connect to the database and create the table
    create_table()

    # Construct API URL
    api_url = f"http://api.weatherstack.com/current?access_key={key}&query={city}"
    
    # Fetch weather data
    data = fetch_api_data(api_url)
    
    if data:
        # Check for API errors
        if "error" in data:
            print(f"API Error: {data['error']}")
            return
            
        print(f"Weather data for {city}:")
        print(data)
        
        # Connect to database and insert data
        conn = connect_to_db()
        if conn:
            try:
                insert_records(conn, data)
            except Exception as e:
                print(f"Error during record insertion: {e}")
            finally:
                conn.close()
        else:
            print("Database connection failed.")
    else:
        print("Failed to retrieve data.")


if __name__ == "__main__":
    main()