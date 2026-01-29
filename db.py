import sqlite3

DB_NAME = "transactions.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            base_price REAL NOT NULL,
            final_price REAL NOT NULL,
            booking_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def insert_booking(category, base_price, final_price, booking_time):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings (category, base_price, final_price, booking_time)
        VALUES (?, ?, ?, ?)
    """, (category, base_price, final_price, booking_time))

    conn.commit()
    conn.close()


def fetch_all_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()
    conn.close()

    bookings = []
    for r in rows:
        bookings.append({
            "id": r["id"],
            "category": r["category"],
            "base_price": r["base_price"],
            "final_price": r["final_price"],
            "booking_time": r["booking_time"]
        })

    return bookings
