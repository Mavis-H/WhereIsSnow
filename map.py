import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from folium.plugins import TimeSliderChoropleth
from branca.element import Figure
import branca.colormap as cm
import webbrowser
from bs4 import BeautifulSoup
import json


# CONST
X_MAP = 44.58
Y_MAP = -103.46
MAX_DAILY_SNOWFALL = 76


# Get map geo dataframe
def prepare_geo_df():
    states_geo = gpd.read_file('geo/cb_2018_us_state_500k.shp')
    states_geo_df = states_geo[['NAME', 'geometry']]
    states_geo_df.rename(columns={'NAME': 'STATE'}, inplace=True)
    states_geo_df['STATE'] = states_geo_df['STATE'].str.replace(' ', '_')
    return states_geo_df


# Get map geo json data
def prepare_geo_json():
    states_geo_df = prepare_geo_df()
    states_geo_json = states_geo_df.set_index('STATE').to_json()
    return states_geo_json


# Assign color and opacity to dataframe, then transfer to dictionary
def generate_style_dict(df):
    bins = np.array([0, 20, 40, 70, 100, 150, 650])
    colors = ['#feebe2', '#fcc5c0', '#fa9fb5', '#f768a1', '#c51b8a', '#7a0177']
    df['COLOR'] = pd.cut(df['VALUE'], bins, labels=colors)
    df['COLOR'] = df['COLOR'].cat.add_categories('#999999').fillna('#999999')

    style_dict = {}
    data_states = set(df['STATE'].unique())
    for state in data_states:
        style_dict[state] = {}
        for values in df[df['STATE']==state].set_index(['STATE']).values:
            style_dict[state][values[1]] = {'color': values[2], 'opacity': 0.8}

    datetimes = df['DATETIME'].unique()
    na_styledict = {dt: {'color': '#999999', 'opacity': 0.8} for dt in datetimes}
    geo_df = prepare_geo_df()
    for state in geo_df['STATE']:
        if state not in data_states:
            style_dict[state] = na_styledict
    return style_dict


# Create map
def create_map():
    mymap = folium.Map(location=[X_MAP, Y_MAP], zoom_start=4, tiles=None)
    folium.TileLayer('Stamen Terrain', name="Light Map", control=False).add_to(mymap)
    return mymap


# Draw timeslider choropleth component
def create_timeslider_choropleth(geo_json, style_dict):
    return TimeSliderChoropleth(
        data=geo_json,
        styledict=style_dict
    )


# Render map
def render_map(mymap):
    mymap.save("map.html")
    webbrowser.open("map.html")


# Draw map according to data
def draw_test_map(df):
    myscale_p48h = (df['VALUE'].quantile((0,0.1,0.75,0.9,1))).tolist()
    map_p48h = folium.Choropleth(
        geo_data=prepare_geo_df(),
        name='US Snow Map 48h',
        data=df,
        columns=['STATE','VALUE'],
        key_on="feature.properties.STATE",
        fill_color='RdPu',
        threshold_scale=myscale_p48h,
        fill_opacity=0.75,
        line_opacity=0.2,
        legend_name='Snow fall accumulation in inches',
        smooth_factor=0,
        nan_fill_color="Black",
        overlay=False
    )
    return map_p48h

# # Add map interaction datails
# style_function = lambda x: {'fillColor': '#ffffff', 
#                             'color':'#000000', 
#                             'fillOpacity': 0.1, 
#                             'weight': 0.1}
# highlight_function = lambda x: {'fillColor': '#000000', 
#                                 'color':'#000000', 
#                                 'fillOpacity': 0.50, 
#                                 'weight': 0.1}
# DATA_p48h = folium.features.GeoJson(
#     data_p48h,
#     style_function=style_function, 
#     control=False,
#     highlight_function=highlight_function, 
#     tooltip=folium.features.GeoJsonTooltip(
#         fields=['STATE','VALUE'],
#         aliases=['State: ','Snow fall accumulation in inches: '],
#         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
#     ),
#     zoom_on_click=True
# )
# mymap.add_child(DATA_p48h)

# # Add snow areas markers
# markerGroup = folium.FeatureGroup(name='Snow Resorts and Areas').add_to(mymap)
# areas = [[uniform(19,65), uniform(-162,-68), uniform(0, 20)] for _ in range(20)]
# for area in areas:
#     markerGroup.add_child(
#         folium.CircleMarker(
#             location=[area[0], area[1]],
#             radius = float(area[2]),
#             popup="Snow Area", # click for contents
#             tooltip = area[2], # hover contents
#             color="black",
#             fill_color="black"
#         )
#     )
# mymap.keep_in_front(markerGroup)

# # Add map layer controller
# folium.LayerControl().add_to(mymap)