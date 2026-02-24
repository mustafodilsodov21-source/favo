import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = "users.db"
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print('Token not found')
else:
    print("Token found")
