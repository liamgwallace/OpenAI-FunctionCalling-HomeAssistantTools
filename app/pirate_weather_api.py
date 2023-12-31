from typing import Optional, List
import requests
import json
from datetime import datetime as dt  
import os
from dotenv import load_dotenv

import requests

def name_to_lat_long(name: str) -> str:
    """
    Converts a place name to a latitude/longitude string using Nominatim geocoding service.

    :param name: The name of the place.
    :return: A string in the format 'latitude,longitude'.
    """
    # Make a request to the Nominatim API
    url = f"https://nominatim.openstreetmap.org/search?q={name}&format=json"
    response = requests.get(url)
    
    # Check if the request was successful and retrieve the coordinates if available
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return f"{latitude},{longitude}"
    
    # Return None if the request fails or no coordinates are found
    return None

def get_weather_forecast(location: str, forecast_type: Optional[List[str]] = None) -> str:
    """
    Gets weather forecast from the Pirate Weather API for one or more specific forecast blocks.
    :param location: Location for which the weather forecast is requested.
    :param forecast_type: A list of forecast blocks for which the weather forecast is requested. Can be 'currently', 'minutely', 'hourly', 'daily', or 'alerts'. If None, data for all forecast blocks will be returned.
    :return: A string representation of the forecast data in CSV format.
    """
    try:
        pirateweather_api_key = os.getenv('pirateweather_api_key')
        # Convert location to latitude and longitude
        lat_long = name_to_lat_long(location)

        # Construct the URL
        url = f'https://api.pirateweather.net/forecast/{pirateweather_api_key}/{lat_long}?units=si'

        all_blocks = ['currently', 'minutely', 'hourly', 'daily', 'alerts']

        # If forecast_type is None, include all blocks
        if forecast_type is None:
            forecast_type = all_blocks
        else:
            excluded_blocks = [block for block in all_blocks if block not in forecast_type]
            exclude_string = ','.join(excluded_blocks)
            url += f'&exclude={exclude_string}'

        # Send a GET request to the Pirate Weather API
        response = requests.get(url)
        # Initialize result
        result = ''

        # If the request was successful, parse the forecast data
        if response.status_code == 200:
            data = response.json()

            # The forecast data structure is different for different forecast blocks
            for block in forecast_type:
                if block in data:
                    result += f"\n{block.capitalize()}:\n"
                    if block == "currently":
                        cur = data[block]
                        cur['time'] = dt.fromtimestamp(cur['time']).strftime('%Y-%m-%d %H:%M:%S')
                        result += ",".join(cur.keys()) + "\n"
                        result += ",".join(map(str, cur.values())) + "\n"
                    elif block == "minutely":
                        mins_data = data[block]['data']
                        if mins_data:
                            minutely_filter = ["time", "precipIntensity", "precipProbability", "precipType"]
                            filtered_header = [header for header in minutely_filter if header in mins_data[0]]
                            result += ",".join(filtered_header) + "\n"
                            for d in mins_data:
                                filtered_data = [str(d.get(key, "")) for key in filtered_header]
                                filtered_data[0] = dt.fromtimestamp(float(filtered_data[0])).strftime('%Y-%m-%d %H:%M:%S')
                                result += ",".join(filtered_data) + "\n"

                    elif block == "hourly":
                        hourly_data = data[block]['data']
                        if hourly_data:
                            hourly_filter = ["time", "summary", "precipIntensity", "precipType", "temperature", "windSpeed", "windBearing", "cloudCover"]
                            filtered_header = [header for header in hourly_filter if header in hourly_data[0]]
                            result += ",".join(filtered_header) + "\n"
                            for d in hourly_data:
                                filtered_data = [str(d.get(key, "")) for key in filtered_header]
                                filtered_data[0] = dt.fromtimestamp(float(filtered_data[0])).strftime('%Y-%m-%d %H:%M:%S')
                                result += ",".join(filtered_data) + "\n"

                    elif block == "daily":
                        daily_data = data[block]['data']
                        if daily_data:
                            daily_filter = ["time", "summary", "precipIntensity", "precipProbability","precipType","windSpeed","windBearing", "cloudCover", "temperatureMin", "temperatureMinTime", "temperatureMax", "temperatureMaxTime"]
                            filtered_header = [header for header in daily_filter if header in daily_data[0]]
                            result += ",".join(filtered_header) + "\n"
                            for d in daily_data:
                                filtered_data = [str(d.get(key, "")) for key in filtered_header]
                                for i, value in enumerate(filtered_data):
                                    if 'time' in filtered_header[i].lower():
                                        filtered_data[i] = dt.fromtimestamp(float(value)).strftime('%Y-%m-%d %H:%M:%S')
                                result += ",".join(filtered_data) + "\n"

            result += f"\nUnits are SI.\nall precip: Millimetres per hour. precipAccumulation: Centimetres. temperatures and dewPoint: Degrees Celsius.all windSpeed: Meters per second. pressure: Hectopascals. visibility: Kilometres."
        else:
            return f"Error: Received status code {response.status_code} from Pirate Weather API"
        return result
    except Exception as e:
        return f"Error: {str(e)}"



# This block is executed only when the module is run directly
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    # Define your API key
    pirateweather_api_key = os.getenv('pirateweather_api_key')

    # Define the location
    location = "Cranleigh, Surrey, England"
    location = "gu67fy"
    # Get the weather forecast
    # print(get_weather_forecast(location, ['currently']))
    # print(get_weather_forecast(location, ['minutely']))
    # print(get_weather_forecast(location, ['hourly']))
    # print(get_weather_forecast(location, ['daily']))
    # print(get_weather_forecast(location, ['alerts']))
    print(get_weather_forecast(location, ['currently', 'minutely','hourly','daily','alerts']))
    # print(get_weather_forecast(location))
    # coordinates = name_to_lat_long(location)
    print(coordinates)


