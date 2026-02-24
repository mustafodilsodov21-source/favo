import aiosqlite
from data import DB_NAME
async def create_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute()
        await db.commit()


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            password TEXT,
            is_logged INTEGER DEFAULT 0
        )
        """)
        await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM users WHERE telegram_id=?",
            (user_id,)
        )
        return await cursor.fetchone()


async def create_user(user_id, password):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO users (telegram_id, password) VALUES (?, ?)",
            (user_id, password)
        )
        await db.commit()


async def login_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET is_logged=1 WHERE telegram_id=?",
            (user_id,)
        )
        await db.commit()


async def logout_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET is_logged=0 WHERE telegram_id=?",
            (user_id,)
        )
        await db.commit()