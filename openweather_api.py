from dotenv import load_dotenv
import os
import requests


load_dotenv()
API_KEY = os.environ['API_KEY']
EXCLUDE = 'current,hourly,minutely,alerts'


def request_8d_snow_rain_forecast(lat, lon):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={EXCLUDE}&appid={API_KEY}'
    response = requests.get(url)
    result = response.json()
    snow_rain_forecast = {}
    for d in result["daily"]:
        values = [0, 0]
        if "snow" in d:
            values[0] = d["snow"]
        if "rain" in d:
            values[1] = d["rain"]
        snow_rain_forecast[d["dt"]] = values
    return snow_rain_forecast