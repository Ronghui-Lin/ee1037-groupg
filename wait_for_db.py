# wait_for_db.py
import time
import psycopg2
from psycopg2 import OperationalError

while True:
    try:
        conn = psycopg2.connect(
            dbname="ticketing_db",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )
        conn.close()
        print("Database is ready.")
        break
    except OperationalError:
        print("Database not ready, waiting...")
        time.sleep(1)
