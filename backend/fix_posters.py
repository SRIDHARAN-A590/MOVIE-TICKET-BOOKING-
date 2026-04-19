import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Official THEATRICAL posters (Strictly 19 Approved Titles)
RELIABLE_POSTERS = {
    "The Batman": "https://img10.hotstar.com/image/upload/f_auto,q_auto/sources/r1/cms/prod/4142/1776237014142-i",
    "Dune": "https://media.newyorker.com/photos/61772f3f7a6eb9892dafd2c1/master/pass/Park-Dune.jpg",
    "Spider-Man: No Way Home": "https://images.indianexpress.com/2021/11/spider-man-no-way-home-1200-2.jpg",
    "Inception": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_g6LtC3x4Ddfav_XPzw-iQ_f4MqlPMkYYuQ&s",
    "Interstellar": "https://m.media-amazon.com/images/I/814E2+pjjzL._AC_SL1500_.jpg",
    "Oppenheimer": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4a/Oppenheimer_%28film%29.jpg/250px-Oppenheimer_%28film%29.jpg",
    "Barbie": "https://upload.wikimedia.org/wikipedia/en/0/0b/Barbie_2023_poster.jpg",
    "Jailer 2": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcREvB05WGBe19rb24kCGUjudps-H63oIAGfcw&s",
    "Leo": "https://images.indianexpress.com/2023/10/leo-review-19102023.jpg",
    "RRR": "https://m.media-amazon.com/images/I/81XSirG7qFL._UF894,1000_QL80_.jpg",
    "Animal": "https://m.media-amazon.com/images/M/MV5BZThmNDg1NjUtNWJhMC00YjA3LWJiMjItNmM4ZDQ5ZGZiN2Y2XkEyXkFqcGc@._V1_.jpg",
    "Pushpa: The Rise": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR43EpXkB8hyRy47_DBdbZI3kmLMxn7dJdjOA&s",
    "Vikram": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQG_4DuNSmYs7fdFTTDdE1TZYwoMYk-RLuNjw&s",
    "Kantara": "https://bloodybrilliant.in/wp-content/uploads/2022/10/Kantara.webp",
    "Varanasi": "https://static.wixstatic.com/media/7c2249_51148a1641404be8b2c70f0d6a9c6905~mv2.jpg/v1/fill/w_672,h_448,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/7c2249_51148a1641404be8b2c70f0d6a9c6905~mv2.jpg",
    "Jana Nayagan": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnlzkOimq2QTp4A0Nbet25xwcy0nr2wmVYDg&s",
    "Ponniyin Selvan: I": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQLPg2otOG3aIP21sU4QB3vMKiS2WLHvnjnWQ&s",
    "Avatar: The Way of Water": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_XLR5oupuwYTeLMinLKBwExRrJ4sXzMYd7w&s",
    "Raaka": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM3CI1Hy5AKqJwtdRFFvhB9zasmQN61ep-PA&s"
}

# Generic theatrical fallback
GENERIC_POSTER = "https://image.tmdb.org/t/p/w500/9Rj8l6gElLpRL7Kj17iZhrT5Zuw.jpg"

def fix_posters():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "movie_booking_system")
        )
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT movie_id, title FROM MOVIES")
        movies = cursor.fetchall()
        
        updated_count = 0
        for movie in movies:
            title = movie['title']
            new_url = RELIABLE_POSTERS.get(title, GENERIC_POSTER)
            cursor.execute("UPDATE MOVIES SET poster_url = %s WHERE movie_id = %s", (new_url, movie['movie_id']))
            updated_count += 1
            
        conn.commit()
        print(f"SUCCESS: Synced {updated_count} approved movie posters.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    fix_posters()
