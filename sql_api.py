import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()
USERNAME = os.environ['PSQL_USERNAME']
PASSWORD = os.environ['PSQL_PASSWORD']
DATABASE = "snow_db"
LOCALHOST = "127.0.0.1"
PORT = 5432

conn = psycopg2.connect(
    dbname=DATABASE, user=USERNAME, password=PASSWORD, host=LOCALHOST, port=PORT
)
cursor = conn.cursor()


def insert_resort_to_db(state, resort, lat, lon, area):
    cursor.execute(
        """
        INSERT INTO resorts (resort, state, lat, lon, area) 
        VALUES (%s, %s, %s, %s, %s) 
        ON CONFLICT (resort) DO NOTHING
        """, 
        (resort, state, lat, lon, area))
    conn.commit()