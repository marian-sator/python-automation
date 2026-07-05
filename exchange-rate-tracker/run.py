import sqlite3
import requests
import time
import os 
from datetime import datetime

timestamps = {}

db = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\database.db")

cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS exchange_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        rate NUMBER
    )
""")

def is_active_hour(hour):
    return hour <= datetime.now().hour < hour + 1

try:

    while True:

        if not is_active_hour(8):
            time.sleep(10)
            continue
        
        dmy = time.strftime('%d.%m.%Y')

        if timestamps.get(dmy, False):
            continue

        try:
            res = requests.get("https://api.frankfurter.dev/v2/rate/USD/EUR", timeout=5)

            if res.status_code != 200:
                print(f"Unreachable - Status: {res.status_code}")
                time.sleep(1)
                continue

            data = res.json()

            if not data or not data.get("rate", False):
                print("Invalid response")
                time.sleep(1)
                continue

            rate = data["rate"]
            timestamp = time.strftime('[%d.%m.%Y %H:%M:%S]')

            print(timestamp, "1 eur =", rate, "usd")

            cursor.execute("""
                INSERT INTO exchange_rates (timestamp, rate)
                VALUES (?, ?)
            """, (timestamp, float(rate)))

            db.commit()

            timestamps[dmy] = True

        except requests.exceptions.Timeout:
            print("Request timed out - Trying again..")

        except requests.exceptions.ConnectionError:
            print("Connection error - Trying again..")

        except Exception as e:
            print(f"Error: {e}")
    
except KeyboardInterrupt:
    print("quit program")

finally:
    db.close()
    print("quit db")

