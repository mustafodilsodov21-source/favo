from aiogram import types
from keyboards.main_menu import main_menu

async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Выбери действие 👇",
        reply_markup=main_menu()
    )