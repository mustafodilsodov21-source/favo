from aiogram import Router, F
from aiogram.types import Message
from services.rates import get_usd, convert_currency
from services.notify import users
from keyboards.main_kb import main_kb

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    users.add(message.from_user.id)
    await message.answer("💱 Бот запущен", reply_markup=main_kb())

@router.message(F.text == "💵 USD")
async def usd(message: Message):
    rate = get_usd()
    await message.answer(f"💵 1 USD = {rate} UZS")

@router.message(F.text == "📊 Курс")
async def kurs(message: Message):
    rate = get_usd()
    await message.answer(f"📊 Текущий курс: {rate} UZS")

@router.message(F.text == "🔢 Конвертер")
async def converter(message: Message):
    await message.answer("Введите сумму и валюту (например: 100 USD)")

    # ожидаем следующий ввод пользователя
    router.message.register(convert_input, F.text)

async def convert_input(message: Message):
    try:
        parts = message.text.split()
        amount = float(parts[0])
        currency = parts[1].upper()
        result = convert_currency(amount, currency)
        await message.answer(f"{amount} {currency} = {result} UZS")
    except:
        await message.answer("❌ Ошибка. Введите, например: 100 USD")