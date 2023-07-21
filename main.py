from ski_resort_scraper import start_scrape
from sql_api import insert_resort_to_db


resorts_dict = start_scrape()
print("INSERTING RESORTS INTO DATABASE")
for state, resorts in resorts_dict.items():
    for resort, data in resorts.items():
        insert_resort_to_db(state, resort, data[0][0], data[0][1], data[1])