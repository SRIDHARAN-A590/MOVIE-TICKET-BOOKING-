import bcrypt, jwt, datetime, os, json, base64
from flask import jsonify
from utils.db import get_db_connection

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwtkey123")

def register_user(data):
    try:
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not name or not email or not password:
            return jsonify({'message': 'All fields are required'}), 400
            
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM USERS WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'message': 'User already exists'}), 400
            
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO USERS (name, email, password_hash, role) VALUES (%s, %s, %s, %s)", 
                       (name, email, hashed_password, 'customer'))
        user_id = cursor.lastrowid
        conn.commit()
        
        token = jwt.encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {'id': user_id, 'name': name, 'email': email, 'role': 'customer'}
        }), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()

def login_user(data):
    try:
        email = data.get('email')
        password = data.get('password')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error. Verify your cloud host settings.'}), 500
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'message': 'Invalid email or password'}), 401
            
        token = jwt.encode({'user_id': user['user_id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {'id': user['user_id'], 'name': user['name'], 'email': user['email'], 'role': user['role']}
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()

