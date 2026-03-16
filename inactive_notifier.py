import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot

# Словарь с последней активностью пользователей
users_activity = {}
bot: Bot = None

async def start_inactive_checker(check_interval_hours: int = 1, inactive_hours: int = 24):
    if bot is None:
        raise RuntimeError("Bot не инициализирован!")

    while True:
        now = datetime.now()
        for user_id, last_active in list(users_activity.items()):
            if now - last_active > timedelta(hours=inactive_hours):
                try:
                    await bot.send_message(
                        user_id,
                        "👋 Привет! Вы давно не заходили в бот. Не пропустите новые Stars и Premium!"
                    )
                    # Обновляем время, чтобы не спамить
                    users_activity[user_id] = now
                except Exception as e:
                    logging.warning(f"Не удалось отправить сообщение {user_id}: {e}")
        await asyncio.sleep(check_interval_hours * 3600)