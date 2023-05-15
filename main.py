import pandas as pd
import numpy as np
from random import uniform
import geopandas as gpd
import folium
from folium.plugins import StripePattern
import branca.colormap as cm
import webbrowser

# CONST
X_MAP = 44.58
Y_MAP = -103.46

# Get map geo data
states = gpd.read_file('geo/cb_2018_us_state_500k.shp')
states = states[['NAME', 'geometry']]

# Get snow data
values_48h = [x for x in range(56)]
values_48h[-1] = np.nan
snow_48h = pd.DataFrame(values_48h, columns=['VALUE'])
snow_48h.insert(0, 'NAME', states['NAME'])

# Merge data by states
data_48h = states.merge(snow_48h, on='NAME')

# Create map
mymap = folium.Map(location=[X_MAP, Y_MAP], zoom_start=4, tiles=None)
folium.TileLayer('Stamen Terrain', name="Light Map", control=False).add_to(mymap)

# Draw map according to data
myscale = (data_48h['VALUE'].quantile((0,0.1,0.75,0.9,1))).tolist()
map_48h = folium.Choropleth(
    geo_data=data_48h,
    name='US Snow Map',
    data=data_48h,
    columns=['NAME','VALUE'],
    key_on="feature.properties.NAME",
    fill_color='RdPu',
    threshold_scale=myscale,
    fill_opacity=0.75,
    line_opacity=0.2,
    legend_name='Snow fall accumulation in inches',
    smooth_factor=0,
    nan_fill_color="White",
    overlay=False
).add_to(mymap)

# Add grey stripe to nan states
nans = data_48h[data_48h['VALUE'].isnull()]
sp = StripePattern(angle=45, color='grey', space_color='white')
sp.add_to(mymap)
folium.GeoJson(
    name='No Snow Zone',
    data=nans,
    style_function=lambda x :{'fillPattern': sp}
    ).add_to(mymap)

# Add map interaction datails
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
DATA = folium.features.GeoJson(
    data_48h,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['NAME','VALUE'],
        aliases=['State: ','Snow fall accumulation in inches: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    ),
    zoom_on_click=True
)
mymap.add_child(DATA)

# Add snow areas markers
markerGroup = folium.FeatureGroup(name='Snow Resorts and Areas').add_to(mymap)
areas = [[uniform(19,65), uniform(-162,-68), uniform(0, 20)] for _ in range(20)]
for area in areas:
    markerGroup.add_child(
        folium.CircleMarker(
            location=[area[0], area[1]],
            radius = float(area[2]),
            popup="Snow Area", # click for contents
            tooltip = area[2], # hover contents
            color="black",
            fill_color="black"
        )
    )
mymap.keep_in_front(markerGroup)

# Add map layer controller
folium.LayerControl().add_to(mymap)

mymap.save("map.html")
webbrowser.open("map.html")