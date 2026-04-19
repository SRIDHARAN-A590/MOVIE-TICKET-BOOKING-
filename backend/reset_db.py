import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def reset():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root")
    )
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS movie_booking_system")
    cursor.execute("CREATE DATABASE movie_booking_system")
    conn.close()
    print("Database reset successfully.")

if __name__ == "__main__":
    reset()
