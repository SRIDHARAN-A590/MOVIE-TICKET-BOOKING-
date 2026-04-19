from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os, jwt
from functools import wraps

from controllers import auth_controller, movie_controller, booking_controller
from controllers import admin_controller
from utils.auth import token_required
from utils.db import get_db_connection

app = Flask(__name__, 
            template_folder='../frontend',
            static_folder='../frontend',
            static_url_path='')
CORS(app)

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwtkey123")

# --- Admin Guard ---
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth = request.headers['Authorization']
            if auth.startswith('Bearer '):
                token = auth.split(" ")[1]
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = data['user_id']
            conn = get_db_connection()
            if not conn:
                return jsonify({'message': 'System Error: Database connection failed. Please check backend logs.'}), 500
            
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT role FROM USERS WHERE user_id=%s", (user_id,))
            user = cursor.fetchone()
            cursor.close(); conn.close()
            if not user or user['role'] != 'admin':
                return jsonify({'message': 'Admin access required'}), 403
        except Exception as e:
            return jsonify({'message': 'Authentication failed or Invalid token'}), 401
        return f(user_id, *args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        if not conn:
            return "Database connection failed. Check your environment variables.", 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MOVIES LIMIT 5")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return str(data)
    except Exception as e:
        return f"Error: {str(e)}", 500

# --- AUTH ROUTES ---
@app.route('/api/auth/register', methods=['POST'])
def register():
    return auth_controller.register_user(request.json)

@app.route('/api/auth/login', methods=['POST'])
def login():
    return auth_controller.login_user(request.json)


@app.route('/api/proxy/image')
def proxy_image():
    url = request.args.get('url')
    if not url: return jsonify({'message': 'URL missing'}), 400
    return movie_controller.proxy_image(url)

# Admin Routes
@app.route('/api/admin/stats_summary')
@admin_required
def get_admin_stats_summary(user_id):
    return admin_controller.admin_get_stats()

@app.route('/api/admin/users')
@admin_required
def get_admin_users():
    return admin_controller.admin_get_users()

# --- MOVIE ROUTES (Public) ---
@app.route('/api/movies', methods=['GET'])
def get_movies():
    return movie_controller.get_all_movies()

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    return movie_controller.get_movie_details(movie_id)

@app.route('/api/movies/<int:movie_id>/shows', methods=['GET'])
def get_shows(movie_id):
    return movie_controller.get_movie_shows(movie_id)

@app.route('/api/shows/<int:show_id>/seats', methods=['GET'])
def get_seats(show_id):
    return movie_controller.get_show_seats(show_id)

# --- USER BOOKING ROUTES ---
@app.route('/api/bookings', methods=['POST'])
@token_required
def create_booking(current_user):
    return booking_controller.create_booking(current_user, request.json)

@app.route('/api/payments', methods=['POST'])
@token_required
def make_payment(current_user):
    return booking_controller.make_payment(current_user, request.json)

@app.route('/api/user/history', methods=['GET'])
@token_required
def get_history(current_user):
    return booking_controller.get_user_history(current_user)

@app.route('/api/bookings/<int:booking_id>/cancel', methods=['POST'])
@token_required
def cancel_booking(current_user, booking_id):
    return booking_controller.cancel_booking(current_user, booking_id)

# =============================================
# ADMIN ROUTES
# =============================================

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def admin_stats(_):
    return admin_controller.get_stats()

# Movies CRUD
@app.route('/api/admin/movies', methods=['POST'])
@admin_required
def admin_add_movie(_):
    return admin_controller.add_movie(request.json)

@app.route('/api/admin/movies/<int:movie_id>', methods=['PUT'])
@admin_required
def admin_update_movie(_, movie_id):
    return admin_controller.update_movie(movie_id, request.json)

@app.route('/api/admin/movies/<int:movie_id>', methods=['DELETE'])
@admin_required
def admin_delete_movie(_, movie_id):
    return admin_controller.delete_movie(movie_id)

# Theatres CRUD
@app.route('/api/admin/theatres', methods=['GET'])
@admin_required
def admin_get_theatres(_):
    return admin_controller.get_all_theatres()

@app.route('/api/admin/theatres', methods=['POST'])
@admin_required
def admin_add_theatre(_):
    return admin_controller.add_theatre(request.json)

@app.route('/api/admin/theatres/<int:theatre_id>', methods=['DELETE'])
@admin_required
def admin_delete_theatre(_, theatre_id):
    return admin_controller.delete_theatre(theatre_id)

# Shows CRUD
@app.route('/api/admin/shows', methods=['GET'])
@admin_required
def admin_get_shows(_):
    return admin_controller.get_all_shows()

@app.route('/api/admin/shows', methods=['POST'])
@admin_required
def admin_add_show(_):
    return admin_controller.add_show(request.json)

@app.route('/api/admin/shows/<int:show_id>', methods=['PUT'])
@admin_required
def admin_update_show(_, show_id):
    return admin_controller.update_show(show_id, request.json)

@app.route('/api/admin/shows/<int:show_id>', methods=['DELETE'])
@admin_required
def admin_delete_show(_, show_id):
    return admin_controller.delete_show(show_id)

# Bookings & Users (read-only)
@app.route('/api/admin/bookings', methods=['GET'])
@admin_required
def admin_get_bookings(_):
    return admin_controller.get_admin_bookings()

@app.route('/api/admin/bookings/<int:booking_id>', methods=['DELETE'])
@admin_required
def admin_cancel_booking(_, booking_id):
    return admin_controller.cancel_booking(booking_id)

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def admin_get_users(_):
    return admin_controller.get_all_users()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
