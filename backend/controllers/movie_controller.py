import requests
from flask import Response, jsonify
from utils.db import get_db_connection

def proxy_image(url):
    try:
        # Fetch the image with a browser-like User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'message': 'Failed to fetch image'}), response.status_code
            
        return Response(
            response.iter_content(chunk_size=1024),
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except Exception as e:
        return jsonify({'message': str(e)}), 500

def get_all_movies():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MOVIES")
        movies = cursor.fetchall()
        return jsonify(movies), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()

def get_movie_details(movie_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MOVIES WHERE movie_id = %s", (movie_id,))
        movie = cursor.fetchone()
        
        if not movie:
            return jsonify({'message': 'Movie not found'}), 404
            
        return jsonify(movie), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()

def get_movie_shows(movie_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.show_id, s.show_time, s.price_base, t.name as theatre_name, t.location 
            FROM SHOWS s
            JOIN THEATRE t ON s.theatre_id = t.theatre_id
            WHERE s.movie_id = %s AND s.show_time > NOW()
            ORDER BY s.show_time ASC
        """
        cursor.execute(query, (movie_id,))
        shows = cursor.fetchall()
        return jsonify(shows), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()

def get_show_seats(show_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Fetch show details along with movie poster
        query = """
            SELECT s.price_base, m.poster_url, m.title 
            FROM SHOWS s
            JOIN MOVIES m ON s.movie_id = m.movie_id
            WHERE s.show_id = %s
        """
        cursor.execute(query, (show_id,))
        show = cursor.fetchone()
        
        if not show:
            return jsonify({'message': 'Show not found'}), 404
            
        base_price = float(show['price_base'])
        poster_url = show['poster_url']
        movie_title = show['title']

        cursor.execute("SELECT seat_id, seat_number, status, seat_type, price_multiplier FROM SEAT WHERE show_id = %s", (show_id,))
        seats = cursor.fetchall()
        return jsonify({
            'seats': seats, 
            'price_base': base_price, 
            'poster_url': poster_url,
            'movie_title': movie_title
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals() and conn: conn.close()
