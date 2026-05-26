import os, mysql.connector
from dotenv import load_dotenv

load_dotenv()

def seed_bookings():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", "3306"))
        )
        cursor = conn.cursor(dictionary=True)
        
        # Get some users
        cursor.execute("SELECT user_id, name, email FROM USERS WHERE role = 'customer' LIMIT 3")
        users = cursor.fetchall()
        
        if not users:
            print("No customers found in database to map bookings.")
            return
            
        # Get the first 3 active shows
        cursor.execute("SELECT show_id, price_base FROM SHOWS LIMIT 3")
        shows = cursor.fetchall()
        
        if not shows:
            print("No shows found in database to map bookings.")
            return

        print("Generating realistic booking and payment history...")
        
        # Clear any existing booking references
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE PAYMENT;")
        cursor.execute("TRUNCATE TABLE BOOKING_SEAT;")
        cursor.execute("TRUNCATE TABLE BOOKING;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()

        payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking']

        for idx, show in enumerate(shows):
            # Pick a customer user
            user = users[idx % len(users)]
            
            # Find 2 available seats for this show
            cursor.execute("SELECT seat_id, seat_number, price_multiplier FROM SEAT WHERE show_id = %s LIMIT 2", (show['show_id'],))
            seats = cursor.fetchall()
            
            if len(seats) < 2:
                continue
                
            # Calculate total amount
            total_amount = sum(float(show['price_base']) * float(seat['price_multiplier']) for seat in seats)
            
            # 1. Insert into BOOKING
            cursor.execute("""
                INSERT INTO BOOKING (user_id, show_id, total_amount, booking_status)
                VALUES (%s, %s, %s, 'Confirmed')
            """, (user['user_id'], show['show_id'], total_amount))
            booking_id = cursor.lastrowid
            
            # 2. Insert into BOOKING_SEAT and update SEAT status to 'Booked'
            for seat in seats:
                cursor.execute("""
                    INSERT INTO BOOKING_SEAT (booking_id, seat_id)
                    VALUES (%s, %s)
                """, (booking_id, seat['seat_id']))
                cursor.execute("""
                    UPDATE SEAT SET status = 'Booked' WHERE seat_id = %s
                """, (seat['seat_id'],))
                
            # 3. Insert into PAYMENT
            method = payment_methods[idx % len(payment_methods)]
            cursor.execute("""
                INSERT INTO PAYMENT (booking_id, amount, payment_method, payment_status)
                VALUES (%s, %s, %s, 'Success')
            """, (booking_id, total_amount, method))
            
        conn.commit()
        print("SUCCESS: 3 active bookings successfully generated!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn: conn.close()

if __name__ == "__main__":
    seed_bookings()
