import mysql.connector

def promote():
    conn = mysql.connector.connect(host='localhost', user='root', password='root', database='movie_booking_system')
    cursor = conn.cursor()
    cursor.execute("UPDATE USERS SET role = 'admin' WHERE email = 'sri@gmail.com'")
    conn.commit()
    print("User sri@gmail.com is now an Administrator.")
    conn.close()

if __name__ == "__main__":
    promote()
