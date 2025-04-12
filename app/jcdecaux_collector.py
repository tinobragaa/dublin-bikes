import requests
import sqlite3
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Your JCDecaux API key
API_KEY = 'c68dab54bda9ba1de22a1c7fc5d29ed1537e33ca'
CONTRACT_NAME = 'dublin'
STATIONS_URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={CONTRACT_NAME}&apiKey={API_KEY}"

DB_PATH = 'instance/stations.db'  # Update if you want to use a different DB

def fetch_and_store():
    print("Fetching data from JCDecaux API...")

    try:
        response = requests.get(STATIONS_URL)
        stations = response.json()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create table if not exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS station_status (
                station_id INTEGER,
                name TEXT,
                bikes_available INTEGER,
                stands_available INTEGER,
                status TEXT,
                timestamp TEXT,
                day TEXT,
                hour INTEGER
            )
        ''')

        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        day = now.strftime('%A')
        hour = now.hour

        for station in stations:
            c.execute('''
                INSERT INTO station_status (
                    station_id, name, bikes_available, stands_available, status, timestamp, day, hour
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                station['number'], station['name'], station['available_bikes'], station['available_bike_stands'],
                station['status'], timestamp, day, hour
            ))

        conn.commit()
        conn.close()
        print("Saved station data.")

    except Exception as e:
        print("Error:", e)

# Start the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store, 'interval', minutes=10)
    scheduler.start()
    print("Scheduler started.")
