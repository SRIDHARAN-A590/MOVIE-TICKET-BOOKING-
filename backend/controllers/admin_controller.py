from flask import jsonify
from utils.db import get_db_connection

# --- Stats ---
def get_stats():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM MOVIES")
        m_count = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM THEATRE")
        t_count = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM USERS")
        u_count = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM BOOKING")
        b_count = cursor.fetchone()['count']
        cursor.execute("SELECT SUM(total_amount) as revenue FROM BOOKING WHERE booking_status = 'Confirmed'")
        total_rev = cursor.fetchone()['revenue'] or 0

        return jsonify({
            'movies': m_count,
            'theatres': t_count,
            'users': u_count,
            'bookings': b_count,
            'revenue': float(total_rev)
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def admin_get_stats(): # Alias for compatibility
    return get_stats()

# --- Revenue Filter by Period ---
def get_revenue_by_period(period):
    """Return revenue filtered by: 'today', 'month', 'year'"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error'}), 500
        cursor = conn.cursor(dictionary=True)

        if period == 'today':
            date_filter = "DATE(b.booking_time) = CURDATE()"
            label = "Today"
        elif period == 'month':
            date_filter = "MONTH(b.booking_time) = MONTH(CURDATE()) AND YEAR(b.booking_time) = YEAR(CURDATE())"
            label = "This Month"
        elif period == 'year':
            date_filter = "YEAR(b.booking_time) = YEAR(CURDATE())"
            label = "This Year"
        else:
            date_filter = "1=1"   # all time
            label = "All Time"

        cursor.execute(f"""
            SELECT 
                COALESCE(SUM(b.total_amount), 0) AS revenue,
                COUNT(b.booking_id)              AS bookings
            FROM BOOKING b
            WHERE b.booking_status = 'Confirmed'
              AND {date_filter}
        """)
        row = cursor.fetchone()
        return jsonify({
            'period': label,
            'revenue': float(row['revenue']),
            'bookings': int(row['bookings'])
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

# --- Movies ---
def add_movie(data):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MOVIES (title, description, duration_mins, genre, language, release_date, poster_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (data['title'], data['description'], data['duration_mins'], data['genre'], data['language'], data['release_date'], data.get('poster_url', '')))
        conn.commit()
        return jsonify({'message': 'Movie added successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def update_movie(movie_id, data):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE MOVIES SET title=%s, description=%s, duration_mins=%s, genre=%s, language=%s, release_date=%s, poster_url=%s
            WHERE movie_id=%s
        """, (data['title'], data['description'], data['duration_mins'], data['genre'], data['language'], data['release_date'], data.get('poster_url', ''), movie_id))
        conn.commit()
        return jsonify({'message': 'Movie updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def delete_movie(movie_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor()
        cursor.execute("DELETE FROM MOVIES WHERE movie_id = %s", (movie_id,))
        conn.commit()
        return jsonify({'message': 'Movie deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

# --- Theatres ---
def get_all_theatres():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM THEATRE")
        res = cursor.fetchall()
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def add_theatre(data):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor()
        cursor.execute("INSERT INTO THEATRE (name, location, total_screens) VALUES (%s, %s, %s)", 
                       (data['name'], data['location'], data.get('total_screens', 1)))
        conn.commit()
        return jsonify({'message': 'Theatre added successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def delete_theatre(theatre_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor()
        cursor.execute("DELETE FROM THEATRE WHERE theatre_id = %s", (theatre_id,))
        conn.commit()
        return jsonify({'message': 'Theatre deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

# --- Shows ---
def get_all_shows():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                s.*,
                m.title as movie_title, 
                t.name as theatre_name,
                COUNT(st.seat_id) as total_seats,
                SUM(CASE WHEN st.status = 'Booked' THEN 1 ELSE 0 END) as booked_seats,
                SUM(CASE WHEN st.status = 'Available' THEN 1 ELSE 0 END) as available_seats
            FROM SHOWS s
            JOIN MOVIES m ON s.movie_id = m.movie_id
            JOIN THEATRE t ON s.theatre_id = t.theatre_id
            LEFT JOIN SEAT st ON s.show_id = st.show_id
            GROUP BY s.show_id, m.title, t.name
            ORDER BY s.show_time DESC
        """
        cursor.execute(query)
        res = cursor.fetchall()
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()


def add_show(data):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error'}), 500
        cursor = conn.cursor()
        
        # 1. Insert Show
        cursor.execute("INSERT INTO SHOWS (movie_id, theatre_id, show_time, price_base) VALUES (%s, %s, %s, %s)",
                       (data['movie_id'], data['theatre_id'], data['show_time'], data['price_base']))
        show_id = cursor.lastrowid
        
        # 2. Populate Seats
        total_seats = int(data.get('total_seats', 50))
        seats_per_row = 10
        seat_insert_data = []
        
        for i in range(total_seats):
            row_char = chr(65 + (i // seats_per_row)) # A, B, C...
            num = (i % seats_per_row) + 1
            seat_number = f"{row_char}{num}"
            
            # Simplified seat types: first 2 rows Gold, rest Silver
            seat_type = 'Gold' if (i // seats_per_row) < 2 else 'Silver'
            multiplier = 1.5 if seat_type == 'Gold' else 1.0
            
            seat_insert_data.append((show_id, seat_number, seat_type, 'Available', multiplier))
            
        cursor.executemany("""
            INSERT INTO SEAT (show_id, seat_number, seat_type, status, price_multiplier)
            VALUES (%s, %s, %s, %s, %s)
        """, seat_insert_data)
        
        conn.commit()
        return jsonify({'message': f'Show scheduled with {total_seats} seats successfully'}), 201
    except Exception as e:
        if 'conn' in locals() and conn: conn.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()


def delete_show(show_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SHOWS WHERE show_id = %s", (show_id,))
        conn.commit()
        return jsonify({'message': 'Show deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def update_show(show_id, data):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE SHOWS SET movie_id=%s, theatre_id=%s, show_time=%s, price_base=%s
            WHERE show_id=%s
        """, (data['movie_id'], data['theatre_id'], data['show_time'], data['price_base'], show_id))
        conn.commit()
        return jsonify({'message': 'Show updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

# --- Bookings & Users ---
def get_admin_bookings():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                b.booking_id, b.user_id, b.show_id,
                CAST(b.total_amount AS CHAR) as total_amount,
                b.booking_status,
                DATE_FORMAT(b.booking_time, '%Y-%m-%d %H:%i:%s') as created_at,
                u.name as user_name, u.email,
                m.title as movie_title,
                t.name as theatre_name
            FROM BOOKING b
            JOIN USERS u ON b.user_id = u.user_id
            JOIN SHOWS s ON b.show_id = s.show_id
            JOIN MOVIES m ON s.movie_id = m.movie_id
            JOIN THEATRE t ON s.theatre_id = t.theatre_id
            ORDER BY b.booking_time DESC
        """
        cursor.execute(query)
        res = cursor.fetchall()
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def cancel_booking(booking_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor()
        cursor.execute("UPDATE BOOKING SET booking_status = 'Cancelled' WHERE booking_id = %s", (booking_id,))
        conn.commit()
        return jsonify({'message': 'Booking cancelled successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def get_all_users():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, role, created_at FROM USERS")
        res = cursor.fetchall()
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()

def admin_get_users(): # Alias for app.py line 67
    return get_all_users()

def admin_get_bookings(): # Alias for app.py line 163 compatibility check
    return get_admin_bookings()
