import os
from dotenv import load_dotenv

load_dotenv()

def promote():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE USERS SET role = 'admin' WHERE email = 'sri@gmail.com'")
    conn.commit()
    print("User sri@gmail.com is now an Administrator.")
    conn.close()

if __name__ == "__main__":
    promote()
