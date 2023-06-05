import requests
from bs4 import BeautifulSoup


# get URL
page = requests.get("https://en.wikipedia.org/wiki/List_of_ski_areas_and_resorts_in_the_United_States")

# scrape webpage
soup = BeautifulSoup(page.content, 'html.parser')
 
# display scraped data
states = soup.find_all('h3')
lists = soup.find('div', class_="mw-parser-output").find_all('ul')[:-2]
print(len(lists))

# for state in states:
#     print(state.contents[0]['id'])
for l in lists[-3:]:
    print(l)
    print('----------------------------')