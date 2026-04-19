import mysql.connector
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def promote_to_admin(email):
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "movie_booking_system")
        )
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT name, role FROM USERS WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"Error: No user found with email '{email}'. Please register first.")
            return

        name, role = user
        if role == 'admin':
            print(f"User '{name}' ({email}) is already an Admin.")
        else:
            cursor.execute("UPDATE USERS SET role = 'admin' WHERE email = %s", (email,))
            conn.commit()
            print(f"SUCCESS: User '{name}' ({email}) has been promoted to Admin!")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python promote_admin.py <email>")
    else:
        promote_to_admin(sys.argv[1])
