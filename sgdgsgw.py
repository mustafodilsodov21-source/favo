
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from data import TOKEN
from wsadfsd import main_kb
import database as db

import asyncio
import hashlib
import logging

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
print(TOKEN)



def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()



class AuthState(StatesGroup):
    waiting_password = State()



@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Добро пожаловать 👋", reply_markup=main_kb)



@router.message(F.text == "📝 Регистрация")
async def register_handler(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if user:
        await message.answer("Ты уже зарегистрирован.")
        return

    await message.answer("Введите пароль:")
    await state.set_state(AuthState.waiting_password)


@router.message(AuthState.waiting_password)
async def process_register(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)

    if not user:
        password = hash_password(message.text)
        await db.create_user(message.from_user.id, password)
        await message.answer("Регистрация успешна ✅", reply_markup=main_kb)
    else:
        if user[1] == hash_password(message.text):
            await db.login_user(message.from_user.id)
            await message.answer("Вход выполнен ✅", reply_markup=main_kb)
        else:
            await message.answer("Неверный пароль ❌")

    await state.clear()



@router.message(F.text == "🔐 Вход")
async def login_handler(message: Message, state: FSMContext):
    await message.answer("Введите пароль:")
    await state.set_state(AuthState.waiting_password)



@router.message(F.text == "👤 Профиль")
async def profile_handler(message: Message):
    user = await db.get_user(message.from_user.id)

    if not user:
        await message.answer("Ты не зарегистрирован.")
        return

    text = (
        f"ID: {user[0]}\n"
        f"Авторизация: {'Да' if user[2] else 'Нет'}"
    )
    await message.answer(text)



@router.message(F.text == "🚪 Выход")
async def logout_handler(message: Message):
    await db.logout_user(message.from_user.id)
    await message.answer("Ты вышел 🚪")



async def main():
    logging.basicConfig(level=logging.INFO)
    await db.init_db()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())