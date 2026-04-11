import time
import pymysql
from django.db import connections
from django.db.utils import OperationalError

print("Waiting for MySQL database...")

while True:
    try:
        conn = connections['default']
        conn.cursor()
        print("Database is available!")
        break
    except OperationalError:
        print("Database unavailable, waiting 1 second...")
        time.sleep(5)
