import pandas as pd
from ski_resort_scraper import scrape_resorts
from openweather_api import request_8d_snow_rain_forecast
from sql_api import *
from map import prepare_geo_json, generate_style_dict, create_map, create_timeslider_choropleth, render_map


ONE_DAY_SECONDS = 86400


# Insert all resorts data once and only once, skip if table already has the data
def insert_resorts(_resorts_dict):
    for state, resorts in _resorts_dict.items():
        for resort, data in resorts.items():
            insert_resort_to_db(state, resort, data[0][0], data[0][1], data[1])


# Get the 8d forcast wheather from openwheather api for each resort
def request_and_upsert_snow_data(_resorts_coordinates_list):
    for resort, lat, lon in _resorts_coordinates_list:
        forecast = request_8d_snow_rain_forecast(lat, lon)
        for dt, [snowfall, rainfall] in forecast.items():
            # upsert_snow_data_to_db(resort, dt, snowfall)
            upsert_rain_data_to_db(resort, dt, rainfall)


# print("START SCRAPING")
# resorts_dict = scrape_resorts()
# print("INSERTING RESORTS INTO DATABASE")
# insert_resorts(resorts_dict)
# replace_state_name()
# print("QUERY RESORTS FROM DB")
# resorts_coordinates_list = get_coordinates_from_db()
# print("REQUESTING 8D FORECAST FROM OPENWEATHER API")
# request_and_upsert_snow_data(resorts_coordinates_list)
# print("FINISHING UPSERT")

# Get aggregated reosrts snowfall of each state
latest_day_start_dt = get_the_latest_rain_dt_from_db() - 6 * 3600
df = pd.DataFrame(columns=['STATE', 'VALUE', 'DATETIME'])
for i in range(7, -1, -1):
    start_dt = latest_day_start_dt - i * ONE_DAY_SECONDS
    end_dt = start_dt + ONE_DAY_SECONDS
    total_rainfall = get_total_rain_from_db(start_dt, end_dt)
    state_df = pd.DataFrame(total_rainfall, columns=['STATE', 'VALUE'])
    state_df['DATETIME'] = start_dt
    df = pd.concat([df, state_df], ignore_index=True)

# Process data for timeslider choropleth map
style_dict = generate_style_dict(df)
geo_json = prepare_geo_json()

# Draw map
mymap = create_map()
tc_component = create_timeslider_choropleth(geo_json, style_dict)
mymap.add_child(tc_component)
render_map(mymap)

