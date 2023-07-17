from dotenv import load_dotenv
import os
import requests


load_dotenv()
API_KEY = os.environ['API_KEY']
EXCLUDE = 'current,hourly,minutely,alerts'

#TODO: get each resort's lat and lon from the db
#TODO: initialize the first batch of 8 day forecast
lat = -46.01
lon = -7.74
url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={EXCLUDE}&appid={API_KEY}'
response = requests.get(url)
result = response.json()
print(result)
# for d in result["daily"]:
#     if "snow" in d:
#         print(d["dt"])

#TODO: request the next 8(th) day data, update once a day
#TODO: shift data column in table to the left