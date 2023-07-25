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


# Initialize resort data
def insert_resort_to_db(state, resort, lat, lon, area):
    cursor.execute(
        """
        INSERT INTO resorts (resort, state, lat, lon, area) 
        VALUES (%s, %s, %s, %s, %s) 
        ON CONFLICT (resort) DO NOTHING
        """, 
        (resort, state, lat, lon, area))
    conn.commit()


# Upsert snowfall data for each resort's 8d forecast
def upsert_snow_data_to_db(data_dict):
    cursor.execute(
        """
        UPDATE snow SET snowfall = %(snowfall)s 
            WHERE resort = %(resort)s AND dt = %(dt)s;
        INSERT INTO snow (resort, dt, snowfall) 
        SELECT %(resort)s, %(dt)s, %(snowfall)s
            WHERE NOT EXISTS (
                SELECT 1 FROM snow 
                WHERE resort = %(resort)s AND dt = %(dt)s
            );
        """, 
        data_dict)
    conn.commit()


def get_coordinates_from_db():
    cursor.execute(
        """
        SELECT resort, lat, lon FROM resorts;
        """)
    data = cursor.fetchall()
    return data