import os, mysql.connector
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def setup_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", "3306"))
        )
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT movie_id, title FROM MOVIES")
        movies = cursor.fetchall()
        cursor.execute("SELECT theatre_id FROM THEATRE")
        theatres = cursor.fetchall()
        
        if not theatres: return

        print("Cleaning up old inventory...")
        cursor.execute("DELETE FROM SEAT")
        cursor.execute("DELETE FROM SHOWS")
        conn.commit()

        show_slots = ["10:00:00", "14:00:00", "18:00:00", "22:00:00"]
        total_shows = 0
        
        print(f"Generating shows for {len(movies)} movies across {len(theatres)} theatres...")
        
        for m_idx, movie in enumerate(movies):
            # Assign each movie to 2 different theatres for better availability
            assigned_theatres = [theatres[m_idx % len(theatres)], theatres[(m_idx + 1) % len(theatres)]]
            
            for theatre in assigned_theatres:
                for t_idx, t_str in enumerate(show_slots):
                    # Stagger by 5 minutes per movie index to avoid UNIQUE constraint on (theatre, time)
                    stagger_mins = m_idx * 5
                    tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                    
                    # Base slot time
                    base_time = datetime.strptime(f"{tomorrow.strftime('%Y-%m-%d')} {t_str}", '%Y-%m-%d %H:%M:%S')
                    actual_time = base_time + timedelta(minutes=stagger_mins)
                    
                    cursor.execute("INSERT INTO SHOWS (movie_id, theatre_id, show_time, price_base) VALUES (%s, %s, %s, 250.00)", 
                                   (movie['movie_id'], theatre['theatre_id'], actual_time.strftime('%Y-%m-%d %H:%M:%S')))
                    show_id = cursor.lastrowid
                    total_shows += 1
                    
                    # Generate 50 Seats
                    seat_types = [('Platinum', 1.5), ('Gold', 1.25), ('Silver', 1.0)]
                    rows = ['A', 'B', 'C', 'D', 'E']
                    for r_idx, row in enumerate(rows):
                        s_type, mult = seat_types[0] if r_idx == 0 else (seat_types[1] if r_idx < 3 else seat_types[2])
                        for col in range(1, 11):
                            cursor.execute("INSERT INTO SEAT (show_id, seat_number, seat_type, price_multiplier) VALUES (%s, %s, %s, %s)",
                                           (show_id, f"{row}{col}", s_type, mult))
            
            if m_idx % 5 == 0:
                conn.commit()
                print(f"Progress: Processed {m_idx} movies...")

        conn.commit()
        print(f"SUCCESS! Created {total_shows} shows with full seat maps.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn: conn.close()

if __name__ == "__main__":
    setup_db()
