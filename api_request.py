import os
import requests
from dotenv import load_dotenv
from typing import Optional

from sqlalchemy import create_engine
engine = create_engine("postgresql://root:root@localhost:5432/weather_db")



load_dotenv()
city: str = "Leipzig"
key: str = os.getenv("WEATHER_API_KEY")

def fetch_api_data(api_url:str, headers=None)-> Optional[dict]:
    """
    Fetch data from a given API URL.

    :param api_url: The URL of the API endpoint.
    :param headers: Optional headers to include in the request.
    :return: The JSON response from the API or None if an error occurs.
    """
    url = f"http://api.weatherstack.com/current?access_key={key}&query={city}"
    try:
        response: object = requests.get(api_url, headers=headers)
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
        connection: object = engine.connect()
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
                connection.execute("""
                    CREATE TABLE IF NOT EXISTS weather_data (
                        id SERIAL PRIMARY KEY,
                        city TEXT,
                        country TEXT,
                        region TEXT,
                        localtime TIMESTAMP,
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
                """)
            print("Table created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            connection.close()

    
def main():
    """
    Main function to execute the API request and print the result.
    """
    api_url = f"http://api.weatherstack.com/current?access_key={key}&query={city}"
    data = fetch_api_data(api_url)
    
    if data:
        print(f"Weather data for {city}:")
        print(data)
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    main()