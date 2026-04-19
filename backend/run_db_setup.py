import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def run_sql_file(filename):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "movie_booking_system")
    )
    cursor = conn.cursor()
    
    with open(filename, 'r') as f:
        content = f.read()
        
    # Split by DELIMITER // logic
    parts = content.split('DELIMITER //')
    
    # Process the first part (regular statements)
    for statement in parts[0].split(';'):
        if statement.strip():
            cursor.execute(statement)
            
    # Process parts with //
    for part in parts[1:]:
        subparts = part.split('DELIMITER ;')
        # subparts[0] contains the body with //
        statements = subparts[0].split('//')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        # subparts[1] contains regular statements after delimiter reset
        if len(subparts) > 1:
            for statement in subparts[1].split(';'):
                if statement.strip():
                    cursor.execute(statement)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Successfully executed {filename}")

if __name__ == "__main__":
    try:
        run_sql_file("database/schema.sql")
        run_sql_file("database/seed.sql")
    except Exception as e:
        print(f"Error: {e}")
