import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from folium.map import Tooltip
from folium.plugins import TimeSliderChoropleth
from TimeSliderChoropleth import MyTimeSliderChoropleth
from branca.colormap import LinearColormap
import webbrowser
from bs4 import BeautifulSoup
import json


# CONST
X_MAP = 44.58
Y_MAP = -103.46
MAX_DAILY_SNOWFALL = 76
BINS = np.array([0, 20, 40, 70, 100, 150, 650])
COLORS = ['#feebe2', '#fcc5c0', '#fa9fb5', '#f768a1', '#c51b8a', '#7a0177']


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
    df['COLOR'] = pd.cut(df['VALUE'], BINS, labels=COLORS)
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


# TODO: modify tooltip style and add popup
# Draw timeslider choropleth component with extended features
def create_interaction(df):
    geo_df = prepare_geo_df()
    data_df = geo_df.merge(df, how='right')
    timestamps = data_df['DATETIME'].unique()
    style_function_dict = {ts: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1} for ts in timestamps}
    style_function = lambda x: style_function_dict
    highlight_function_dict = {ts: {'fillColor': '#004560', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1} for ts in timestamps}
    highlight_function = lambda x: highlight_function_dict
    # tooltip = folium.features.GeoJsonTooltip(
    #         fields=[],
    #         aliases=[],
    #         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    #     )
    tooltips = {ts: Tooltip(text="hello") for ts in timestamps}
    return MyTimeSliderChoropleth(
        data=data_df,
        timestamps=timestamps,
        style_function=style_function,
        highlight_function=highlight_function,
        control=False,
        tooltips=tooltips,
        zoom_on_click=True
    )


# Render map
def render_map(mymap):
    mymap.save("map.html")
    webbrowser.open("map.html")


# Draw map legend using choropleth
def create_legend(df):
    map_legend = folium.Choropleth(
        geo_data=prepare_geo_df(),
        name='Legend',
        data=df,
        columns=['STATE','VALUE'],
        key_on="feature.properties.STATE",
        fill_color='RdPu',
        threshold_scale=BINS,
        fill_opacity=0.0,
        line_opacity=0.0,
        legend_name='Snow fall accumulation in inches',
        overlay=False
    )
    return map_legend


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