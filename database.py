import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            amount INTEGER,
            price INTEGER
        )
    """)
    conn.commit()

def add_order(user_id, username, amount, price):
    cursor.execute("""
        INSERT INTO orders (user_id, username, amount, price)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, amount, price))
    conn.commit()

def get_orders():
    cursor.execute("SELECT * FROM orders")
    return cursor.fetchall()