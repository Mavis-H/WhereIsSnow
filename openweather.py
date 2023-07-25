from dotenv import load_dotenv
import os
import requests


load_dotenv()
API_KEY = os.environ['API_KEY']
EXCLUDE = 'current,hourly,minutely,alerts'


def request_8d_snow_forecast(lat, lon):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={EXCLUDE}&appid={API_KEY}'
    response = requests.get(url)
    result = response.json()
    snow_forecast = {}
    for d in result["daily"]:
        if "snow" in d:
            snow_forecast[d["dt"]] = d["snow"]
        else:
            snow_forecast[d["dt"]] = 0
    return snow_forecast