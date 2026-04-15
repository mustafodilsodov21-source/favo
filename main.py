import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from config import BOT_TOKEN
from handlers.start import start_handler

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start_handler, Command("start"))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
