"""
Helper script to create an admin user directly in the database.
Run this once after setting up the schema:
    python create_admin.py
"""
import os
import bcrypt
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

print("=== CineTick Admin User Creator ===")
name  = input("Admin Name [Admin]: ").strip() or "Admin"
email = input("Admin Email [admin@cinetick.com]: ").strip() or "admin@cinetick.com"
pwd   = input("Admin Password [Admin@123]: ").strip() or "Admin@123"

hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT", "3306"))
)
cursor = conn.cursor()

cursor.execute("SELECT user_id FROM USERS WHERE email=%s", (email,))
existing = cursor.fetchone()

if existing:
    cursor.execute("UPDATE USERS SET role='admin', password_hash=%s WHERE email=%s", (hashed, email))
    print(f"[✓] Updated existing user '{email}' to admin role.")
else:
    cursor.execute(
        "INSERT INTO USERS (name, email, password_hash, role) VALUES (%s,%s,%s,'admin')",
        (name, email, hashed)
    )
    print(f"[✓] Created admin user '{email}' successfully.")

conn.commit()
cursor.close()
conn.close()
print("Done! You can now log in at admin-login.html")
