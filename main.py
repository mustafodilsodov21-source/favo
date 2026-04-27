import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from keyboard import main_keyboard, language_keyboard
from gpt import ask_gpt
from db import Database

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

db = Database()

LIMIT = 20


@router.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id

    db.ensure_user(user_id)

    await message.answer(
        "Выберите язык / Tilni tanlang / Choose language",
        reply_markup=language_keyboard
    )


@router.message(F.text.in_(["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"]))
async def choose_lang(message: Message):
    user_id = message.from_user.id
    db.ensure_user(user_id)

    if "🇺🇿" in message.text:
        db.set_language(user_id, "uz")
        text = "Til tanlandi 🇺🇿"
    elif "🇷🇺" in message.text:
        db.set_language(user_id, "ru")
        text = "Язык выбран 🇷🇺"
    else:
        db.set_language(user_id, "en")
        text = "Language selected 🇬🇧"

    await message.answer(text, reply_markup=main_keyboard)


@router.message(F.text == "🧹 Очистить память")
async def clear(message: Message):
    user_id = message.from_user.id
    db.clear_history(user_id)
    await message.answer("Память очищена 🧹")


@router.message()
async def gpt_handler(message: Message):
    user_id = message.from_user.id
    db.ensure_user(user_id)

    if db.get_requests(user_id) >= LIMIT:
        await message.answer("Лимит запросов исчерпан 😢")
        return

    db.increment_requests(user_id)

    lang = db.get_language(user_id)
    text = message.text

    if lang == "uz":
        text = f"Ответь на узбекском: {text}"
    elif lang == "ru":
        text = f"Ответь на русском: {text}"
    else:
        text = f"Answer in English: {text}"

    answer = await ask_gpt(user_id, text)

    await message.answer(answer)


async def main():
    db.create_tables()

    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())