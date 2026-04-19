import os, bcrypt
from dotenv import load_dotenv

load_dotenv()

def seed_users():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", "3306"))
        )
        cursor = conn.cursor()
        
        # Clear users for a clean start if needed, or just update/insert
        print("Seeding authenticated users...")
        
        users_to_seed = [
            ('Administrator', 'admin@cinetick.com', 'Admin@123', 'admin'),
            ('Sridharan', 'sri@gmail.com', '123', 'admin'),
            ('Test User', 'test@cinetick.com', '123', 'customer')
        ]
        
        for name, email, password, role in users_to_seed:
            # Check if exists
            cursor.execute("SELECT user_id FROM USERS WHERE email = %s", (email,))
            exists = cursor.fetchone()
            
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if exists:
                cursor.execute("UPDATE USERS SET name=%s, password_hash=%s, role=%s WHERE email=%s", 
                               (name, hashed, role, email))
            else:
                cursor.execute("INSERT INTO USERS (name, email, password_hash, role) VALUES (%s, %s, %s, %s)", 
                               (name, email, hashed, role))
        
        conn.commit()
        print("SUCCESS: Users seeded with secure bcrypt hashes.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn: conn.close()

if __name__ == "__main__":
    seed_users()
