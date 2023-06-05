import pandas as pd
import numpy as np
from random import uniform
import geopandas as gpd
import folium
from folium.plugins import StripePattern, TimeSliderChoropleth
import branca.colormap as cm
import webbrowser

#TODO: data preprocessing for time slider choropleth
# CONST
X_MAP = 44.58
Y_MAP = -103.46
MAX_DAILY_SNOWFALL = 76

# Get map geo data
states = gpd.read_file('geo/cb_2018_us_state_500k.shp')
states = states[['NAME', 'geometry']]

# Get snow data
values_p48h = [uniform(0, 2 * MAX_DAILY_SNOWFALL) for _ in range(56)]
values_p48h[-1] = np.nan
snow_p48h = pd.DataFrame(values_p48h, columns=['VALUE'])
snow_p48h.insert(0, 'NAME', states['NAME'])

values_f48h = [uniform(0, 2 * MAX_DAILY_SNOWFALL) for _ in range(56)]
values_f48h[-3] = np.nan
snow_f48h = pd.DataFrame(values_f48h, columns=['VALUE'])
snow_f48h.insert(0, 'NAME', states['NAME'])

values_8d = [uniform(0, 8 * MAX_DAILY_SNOWFALL) for _ in range(56)]
values_8d[-2] = np.nan
snow_8d = pd.DataFrame(values_8d, columns=['VALUE'])
snow_8d.insert(0, 'NAME', states['NAME'])

# Assign color
bins = np.array([0, 20, 40, 70, 100, 150, 650])
colors = ['#feebe2', '#fcc5c0', '#fa9fb5', '#f768a1', '#c51b8a', '#7a0177']
snow_p48h['COLOR'] = pd.cut(snow_p48h['VALUE'], bins, labels=colors)
snow_p48h['COLOR'] = snow_p48h['COLOR'].cat.add_categories('#999999').fillna('#999999')
print(snow_p48h)

# # Create map
# mymap = folium.Map(location=[X_MAP, Y_MAP], zoom_start=4, tiles=None)
# folium.TileLayer('Stamen Terrain', name="Light Map", control=False).add_to(mymap)

# # Draw map according to data
# myscale_p48h = (data_p48h['VALUE'].quantile((0,0.1,0.75,0.9,1))).tolist()
# map_p48h = folium.Choropleth(
#     geo_data=data_p48h,
#     name='US Snow Map 48h',
#     data=data_p48h,
#     columns=['NAME','VALUE'],
#     key_on="feature.properties.NAME",
#     fill_color='RdPu',
#     threshold_scale=myscale_p48h,
#     fill_opacity=0.75,
#     line_opacity=0.2,
#     legend_name='Snow fall accumulation in inches',
#     smooth_factor=0,
#     nan_fill_color="Black",
#     overlay=False
# ).add_to(mymap)

# # # Add grey stripe to nan states
# # nans = data_48h[data_48h['VALUE'].isnull()]
# # sp = StripePattern(angle=45, color='grey', space_color='white')
# # sp.add_to(mymap)
# # folium.GeoJson(
# #     name='No Snow Zone',
# #     data=nans,
# #     style_function=lambda x :{'fillPattern': sp}
# #     ).add_to(mymap)

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
#         fields=['NAME','VALUE'],
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

# mymap.save("map.html")
# webbrowser.open("map.html")