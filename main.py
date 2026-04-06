import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from config import TOKEN
from handlers.user import router as user_router
from handlers.admin import router as admin_router
from services.notify import last_rate, users
from services.rates import get_usd

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

async def notifier():
    global last_rate
    while True:
        try:
            rate = get_usd()
            if last_rate and rate != last_rate:
                for user_id in users:
                    await bot.send_message(user_id, f"📢 Курс обновлен: {rate} UZS")
            last_rate = rate
        except Exception as e:
            print(e)
        await asyncio.sleep(300)

async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(user_router)
    dp.include_router(admin_router)
    asyncio.create_task(notifier())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


