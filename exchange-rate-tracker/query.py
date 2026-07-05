import sqlite3
import os 

db = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\exchange_rates.db")

cursor = db.cursor()

cursor.execute("SELECT timestamp, MIN(rate) FROM exchange_rates")
timestamp, min_rate = cursor.fetchone()
print(f"{timestamp} Lowest rate: 1$ = {min_rate}€")

cursor.execute("SELECT timestamp, MAX(rate) FROM exchange_rates")
timestamp, max_rate = cursor.fetchone()
print(f"{timestamp} Highest rate: 1$ = {max_rate}€")

cursor.execute("SELECT AVG(rate) FROM exchange_rates")
avg_rate = cursor.fetchone()[0]
print(f"Average: 1$ = {avg_rate}€")
