import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", "3306")

    if not all([host, user, database]):
        print("CRITICAL: Missing Database Environment Variables (DB_HOST, DB_USER, or DB_NAME)")
        return None

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port)
        )
        return conn
    except mysql.connector.Error as err:
        print(f"DATABASE CONNECTION ERROR: {err}")
        return None
