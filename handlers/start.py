import sqlite3

conn = sqlite3.connect("favo.db", check_same_thread=False)
cursor = conn.cursor()


def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        role TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()


def save_message(user_id, username, role, content):
    try:
        cursor.execute(
            "INSERT INTO messages (user_id, username, role, content) VALUES (?, ?, ?, ?)",
            (user_id, username, role, content)
        )
        conn.commit()
        print("SAVED:", user_id, role, content)
    except Exception as e:
        print("DB ERROR:", e)


def get_history(user_id, limit=10):
    cursor.execute(
        "SELECT role, content FROM messages WHERE user_id=? ORDER BY id DESC LIMIT ?",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]