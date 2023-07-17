import requests
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
import pandas as pd


WIKI_MAIN_URL = "https://en.wikipedia.org"

# Filter sub ski areas from ski areas list
def none_nested_li(tag):
    return tag.name == 'li' and tag.parent.parent.name != 'li'

# Select the correct table from all tables
def select_table(_tables):
    table = None
    for t in _tables:
        cats = t.iloc[:,0].unique()
        if "Coordinates" in cats and "Skiable area" in cats:
            table = t
            break
    return table

# Process string coordinates data to number format
def format_coordinates(coordinates):
    # Latitude
    lat = coordinates[0].split(chr(176))
    lat_num = lat[0]
    lat_dir = lat[1][0]
    coordinates[0] = -float(lat_num) if lat_dir == 'S' else float(lat_num)
    # Longtitude
    lon = coordinates[1].split(chr(176))
    lon_num = lon[0]
    lon_dir = lon[1][0]
    coordinates[1] = -float(lon_num) if lon_dir == 'W' else float(lon_num)
    return coordinates

# Get datail data for each ski area
def get_details(resort):
    a = len(resort.find_all('a'))
    # No linked wiki of this resort or the only link is for the resort location
    if a == 0 or (a == 1 and isinstance(resort.find('a').previous_element, NavigableString)):
        return None, None, None
    else:
        resort_name = resort.find('a')['title']
        print(resort_name)
        sublink = resort.find('a')['href']
        # Page not found
        if 'redlink=1' in sublink:
            return resort_name, None, None
        link = WIKI_MAIN_URL + sublink
        # Handle exception when no table is found
        tables = []
        try:
            tables = pd.read_html(link, attrs = {"class":"infobox vcard"})
        except ValueError:
            return resort_name, None, None
        # Select the correct vbox
        resort_info = select_table(tables)
        # No coordiantes or area found
        if resort_info is None:
            return resort_name, None, None
        # Extract coordinates and area data from the table
        str_coordinates = resort_info[resort_info.iloc[:,0]=="Coordinates"].iloc[:,1].values[0].replace('\ufeff', '').split()[-2:]
        coordinates = format_coordinates(str_coordinates)
        str_area = resort_info[resort_info.iloc[:,0]=="Skiable area"].iloc[:,1].values[0].split()[0]
        area = float(re.sub('[^0-9.]+', '', str_area)) # acres
        return resort_name, coordinates, area

# Insert ski area into the dictionary
def insert_ski_resort(_states_dict, _state_name, _resorts):
    single_state_dict = {}
    print('----------------')
    print(_state_name)
    for resort in _resorts:
        resort_name, coordinates, area = get_details(resort)
        if coordinates != None:
            single_state_dict[resort_name] = [coordinates, area]
    _states_dict[_state_name] = single_state_dict
    return _states_dict

# Initialize data dictionary
states_dict = {}

# Get page from URL
page = requests.get("https://en.wikipedia.org/wiki/List_of_ski_areas_and_resorts_in_the_United_States")

# Scrape webpage
soup = BeautifulSoup(page.content, 'html.parser')
 
# Searched for desired data
body = soup.find('div', class_="mw-parser-output")

# Start point
state = body.find('h2')

# Scrape the complete list
while True:
    state = state.find_next_sibling('h3')
    if state == None:
        break
    state_name = state.contents[0]['id']
    resorts = state.find_next_sibling('ul').find_all('li')
    insert_ski_resort(states_dict, state_name, resorts)
count = 0
for value in states_dict.values():
    count += len(value)
print(count)
print(states_dict)