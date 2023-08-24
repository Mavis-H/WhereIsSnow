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
        (resort, state, lat, lon, area)
    )
    conn.commit()


# Upsert snowfall data for each resort's 8d forecast
def upsert_snow_data_to_db(resort, dt, snowfall):
    cursor.execute(
        """
        UPDATE snow SET snowfall = %(snowfall)s 
            WHERE resort = %(resort)s AND dt = %(dt)s;
        INSERT INTO snow (resort, dt, snowfall) 
        SELECT %(resort)s, %(dt)s, %(snowfall)s
            WHERE NOT EXISTS (
                SELECT 1 
                FROM snow 
                WHERE resort = %(resort)s AND dt = %(dt)s
            );
        """, 
        {'resort': resort, 'dt': dt, 'snowfall': snowfall}
    )
    conn.commit()


# Upsert rainfall data for each resort's 8d forecast
def upsert_rain_data_to_db(resort, dt, rainfall):
    cursor.execute(
        """
        UPDATE rain SET rainfall = %(rainfall)s 
            WHERE resort = %(resort)s AND dt = %(dt)s;
        INSERT INTO rain (resort, dt, rainfall) 
        SELECT %(resort)s, %(dt)s, %(rainfall)s
            WHERE NOT EXISTS (
                SELECT 1 
                FROM rain 
                WHERE resort = %(resort)s AND dt = %(dt)s
            );
        """, 
        {'resort': resort, 'dt': dt, 'rainfall': rainfall}
    )
    conn.commit()


def get_coordinates_from_db():
    cursor.execute(
        """
        SELECT resort, lat, lon 
        FROM resorts;
        """
    )
    data = cursor.fetchall()
    return data


def get_the_latest_rain_dt_from_db():
    cursor.execute(
        """
        SELECT MAX(dt) 
        FROM rain;
        """
    )
    data = cursor.fetchone()[0]
    return data


def get_total_rain_from_db(start_dt, end_dt):
    cursor.execute(
        """
        SELECT state, SUM(rainfall) 
        FROM rain
        JOIN resorts ON rain.resort = resorts.resort
        WHERE dt >= %s AND dt < %s
        GROUP BY state;
        """,
        (start_dt, end_dt)
    )
    data = cursor.fetchall()
    return data


# Update all state name in db to use _ instead of white space
def replace_state_name():
    cursor.execute(
        """
        UPDATE resorts SET state = REPLACE(state, ' ', '_');
        """
    )
    conn.commit()