from ski_resort_scraper import start_scrape
from openweather_api import request_8d_snow_rain_forecast
from sql_api import insert_resort_to_db, get_coordinates_from_db, upsert_snow_data_to_db, upsert_rain_data_to_db, get_the_latest_rain_dt_from_db, get_total_rain_from_db


# # Insert all resorts data once and only once, skip if table already has the data
# resorts_dict = start_scrape()
# print("INSERTING RESORTS INTO DATABASE")
# for state, resorts in resorts_dict.items():
#     for resort, data in resorts.items():
#         insert_resort_to_db(state, resort, data[0][0], data[0][1], data[1])

TEST_LAT = -46.01
TEST_LON = -7.74
ONE_DAY_SECONDS = 86400

# # Get the 8d forcast wheather from openwheather api for each resort
# print("QUERY RESORTS FROM DB")
# resorts_coordinates_list = get_coordinates_from_db()
# print("REQUESTING 8D FORECAST FROM OPENWEATHER API")
# count = 0
# for resort, lat, lon in resorts_coordinates_list:
#     forecast = request_8d_snow_rain_forecast(lat, lon)
#     for dt, [snowfall, rainfall] in forecast.items():
#         upsert_snow_data_to_db(resort, dt, snowfall)
#         upsert_rain_data_to_db(resort, dt, rainfall)
# print("FINISHING UPSERT")

# Get aggregated reosrts snowfall of each state
latest_day_start_dt = get_the_latest_rain_dt_from_db() - 6 * 3600
style_dict = {}
for i in range(7, -1, -1):
    start_dt = latest_day_start_dt - i * ONE_DAY_SECONDS
    end_dt = start_dt + ONE_DAY_SECONDS
    total_rainfall = get_total_rain_from_db(start_dt, end_dt)
    for state, rainfall in total_rainfall:
        if state not in style_dict:
            style_dict[state] = {}
        style_dict[state][start_dt] = rainfall
print(style_dict)