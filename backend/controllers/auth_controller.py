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


def google_login_user(data):
    try:
        credential = data.get('credential')
        if not credential:
            return jsonify({'message': 'Credential is required'}), 400
            
        # Decode token without verification to get user info (email and name)
        # Note: In a production environment, you should verify the JWT signature.
        try:
            decoded = jwt.decode(credential, options={"verify_signature": False})
        except Exception as jwt_err:
            return jsonify({'message': f'Invalid token structure: {str(jwt_err)}'}), 400
            
        email = decoded.get('email')
        name = decoded.get('name') or (decoded.get('email', '').split('@')[0] if decoded.get('email') else 'Google User')
        
        if not email:
            return jsonify({'message': 'Email not found in token'}), 400
            
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection error.'}), 500
            
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            # Create a new user since they don't exist
            # For OAuth users, we can generate a random password hash or set it to a dummy value
            dummy_password = bcrypt.hashpw(os.urandom(16), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("INSERT INTO USERS (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                           (name, email, dummy_password, 'customer'))
            conn.commit()
            user_id = cursor.lastrowid
            role = 'customer'
        else:
            user_id = user['user_id']
            name = user['name']
            role = user['role']
            
        # Generate our own local JWT token for subsequent API requests
        token = jwt.encode({'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, JWT_SECRET, algorithm="HS256")
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {'id': user_id, 'name': name, 'email': email, 'role': role}
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()
