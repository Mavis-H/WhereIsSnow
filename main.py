from ski_resort_scraper import start_scrape
from openweather import request_8d_snow_forecast
from sql_api import insert_resort_to_db, get_coordinates_from_db, upsert_snow_data_to_db


# # Insert all resorts data once and only once, skip if table already has the data
# resorts_dict = start_scrape()
# print("INSERTING RESORTS INTO DATABASE")
# for state, resorts in resorts_dict.items():
#     for resort, data in resorts.items():
#         insert_resort_to_db(state, resort, data[0][0], data[0][1], data[1])

TEST_LAT = -46.01
TEST_LON = -7.74

# Get the 8d forcast wheather from openwheather api for each resort
print("QUERY RESORTS FROM DB")
resorts_coordinates_list = get_coordinates_from_db()
print("REQUESTING 8D FORECAST FROM OPENWEATHER API")
count = 0
for resort, lat, lon in resorts_coordinates_list:
    forecast = request_8d_snow_forecast(lat, lon)
    for dt, snowfall in forecast.items():
        upsert_snow_data_to_db({'resort': resort, 'dt': dt, 'snowfall': snowfall})
print("FINISHING UPSERT")