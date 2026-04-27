import sqlite3
import os


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        os.makedirs(os.path.dirname(self.path_to_db) or ".", exist_ok=True)
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql, parameters=(), fetchone=False, fetchall=False, commit=False):
        conn = self.connection
        cursor = conn.cursor()

        cursor.execute(sql, parameters)

        data = None
        if commit:
            conn.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        conn.close()
        return data

    # 🧱 USERS
    def create_tables(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'ru',
            requests INTEGER DEFAULT 0
        )
        """, commit=True)

        self.execute("""
        CREATE TABLE IF NOT EXISTS Messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            content TEXT
        )
        """, commit=True)

    # 💬 messages
    def add_message(self, user_id, role, content):
        self.execute(
            "INSERT INTO Messages (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content),
            commit=True
        )

    def get_history(self, user_id):
        rows = self.execute(
            "SELECT role, content FROM Messages WHERE user_id=? ORDER BY id ASC LIMIT 20",
            (user_id,),
            fetchall=True
        )

        return [{"role": r[0], "content": r[1]} for r in rows]

    def clear_history(self, user_id):
        self.execute(
            "DELETE FROM Messages WHERE user_id=?",
            (user_id,),
            commit=True
        )

    # 👤 user language
    def set_language(self, user_id, lang):
        self.execute(
            "UPDATE Users SET language=? WHERE id=?",
            (lang, user_id),
            commit=True
        )

    def get_language(self, user_id):
        row = self.execute(
            "SELECT language FROM Users WHERE id=?",
            (user_id,),
            fetchone=True
        )
        return row[0] if row else "ru"

    # 📊 requests
    def increment_requests(self, user_id):
        self.execute(
            "UPDATE Users SET requests = requests + 1 WHERE id=?",
            (user_id,),
            commit=True
        )

    def get_requests(self, user_id):
        row = self.execute(
            "SELECT requests FROM Users WHERE id=?",
            (user_id,),
            fetchone=True
        )
        return row[0] if row else 0

    # ➕ create user if not exists
    def ensure_user(self, user_id):
        self.execute(
            "INSERT OR IGNORE INTO Users (id) VALUES (?)",
            (user_id,),
            commit=True
        )


def logger(statement):
    print(statement)


