from flask import jsonify
from utils.db import get_db_connection

def create_booking(user_id, data):
    try:
        show_id = data.get('show_id')
        seat_ids = data.get('seat_ids') # list of seat IDs
        
        if not all([show_id, seat_ids]) or not isinstance(seat_ids, list):
            return jsonify({'message': 'Invalid booking data'}), 400
            
        conn = get_db_connection()
        if not conn: return jsonify({'message': 'DB Error'}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        # Calculate amount and check seat availability
        format_strings = ','.join(['%s'] * len(seat_ids))
        cursor.execute(f"SELECT seat_id, price_multiplier, status FROM SEAT WHERE seat_id IN ({format_strings}) AND show_id = %s", (*seat_ids, show_id))
        seats = cursor.fetchall()
        
        if len(seats) != len(seat_ids) or any(seat['status'] != 'Available' for seat in seats):
            return jsonify({'message': 'Some seats are not available'}), 400
            
        cursor.execute("SELECT price_base FROM SHOWS WHERE show_id = %s", (show_id,))
        show = cursor.fetchone()
        
        # Calculate total price using multipliers
        total_amount = sum(float(show['price_base']) * float(seat['price_multiplier']) for seat in seats)
        
        # Apply discount using Function if applicable
        cursor.execute("SELECT Calculate_Discount(%s) AS discount", (total_amount,))
        discount = cursor.fetchone()['discount']
        final_amount = float(total_amount) - float(discount)
        
        # Create Booking
        cursor.execute("INSERT INTO BOOKING (user_id, show_id, total_amount, booking_status) VALUES (%s, %s, %s, 'Confirmed')", 
                       (user_id, show_id, final_amount))
        booking_id = cursor.lastrowid
        
        # Insert Booking Seats (This will fire the Trigger to update seat status)
        for seat_id in seat_ids:
            cursor.execute("INSERT INTO BOOKING_SEAT (booking_id, seat_id) VALUES (%s, %s)", (booking_id, seat_id))
            
        conn.commit()
        
        return jsonify({
            'message': 'Booking successful', 
            'booking_id': booking_id, 
            'amount_paid': final_amount,
            'discount_applied': discount
        }), 201
        
    except Exception as e:
        if 'conn' in locals() and conn: conn.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()

def make_payment(user_id, data):
    try:
        booking_id = data.get('booking_id')
        payment_method = data.get('payment_method')
        amount = data.get('amount')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM BOOKING WHERE booking_id = %s AND user_id = %s", (booking_id, user_id))
        if not cursor.fetchone():
            return jsonify({'message': 'Invalid booking'}), 404
        # Map generic method names to DB ENUM values
        method_map = {
            'Card': 'Credit Card',
            'Debit Card': 'Debit Card',
            'Credit Card': 'Credit Card',
            'UPI': 'UPI',
            'Net Banking': 'Net Banking'
        }
        actual_method = method_map.get(payment_method, 'Credit Card')
            
        cursor.execute("INSERT INTO PAYMENT (booking_id, amount, payment_method, payment_status) VALUES (%s, %s, %s, 'Success')",
                       (booking_id, amount, actual_method))
        conn.commit()
        return jsonify({'message': 'Payment successful'}), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()

def get_user_history(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Using View here
        cursor.execute("SELECT * FROM View_User_Booking_Details WHERE email = (SELECT email FROM USERS WHERE user_id = %s)", (user_id,))
        bookings = cursor.fetchall()
        return jsonify(bookings), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()

def cancel_booking(user_id, booking_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check ownership and status
        cursor.execute("SELECT booking_status FROM BOOKING WHERE booking_id = %s AND user_id = %s", (booking_id, user_id))
        booking = cursor.fetchone()
        
        if not booking:
            return jsonify({'message': 'Booking not found'}), 404
        if booking['booking_status'] == 'Cancelled':
            return jsonify({'message': 'Already cancelled'}), 400
            
        cursor.execute("UPDATE BOOKING SET booking_status = 'Cancelled' WHERE booking_id = %s", (booking_id,))
        conn.commit()
        return jsonify({'message': 'Ticket cancelled successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn: conn.close()
