import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from wsadfsd import phone_keyboard

TOKEN = "8255670538:AAHPIcZX1-LKHPYT3uuP9s5EM_qioaVjYbo"

bot = Bot(TOKEN)
dp = Dispatcher()
router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "▶️Нажми кнопку, чтобы отправить номер телефона",
        reply_markup=phone_keyboard()
    )


@router.message(F.contact)
async def get_phone(message: Message):
    phone = message.contact.phone_number
    user = message.from_user.full_name


    print(f"Имя: {user}, Номер: {phone}")

    await message.answer(
        f"Спасибо! Я получил твой номер:\n{phone}"
    )


async def main():
    dp.include_router(router)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())