import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command

from keyboards import start_keyboard, premium_options_keyboard, stars_options_keyboard
from inactive_notifier import start_inactive_checker, users_activity

import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")
MANAGER_USERNAME = os.getenv("MANAGER_USERNAME")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()
router = Router()



orders = []


premium_prices = {
    "3 месяца — 170 000": 170000 * 100,
    "6 месяцев — 220 000": 220000 * 100,
    "12 месяцев — 390 000": 390000 * 100
}

stars_prices = {
    "50 stars — 12 000": 12000 * 100,
    "100 stars — 24 000": 24000 * 100
}


@router.message(Command(commands=["start"]))
async def start(message: Message):
    users_activity[message.from_user.id] = datetime.now()
    await message.answer(
        "Добро пожаловать 👋\nВыберите товар:",
        reply_markup=start_keyboard()
    )


@router.message(F.text == "💎 Telegram Premium")
async def premium(message: Message):
    users_activity[message.from_user.id] = datetime.now()
    await message.answer_photo(
        photo="AgACAgIAAxkBAANuaX9Gyg-D6cJWLQ0o3AWtz9MyKYsAAocQaxsvc_hL7BTeWIu8d_YBAAMCAAN4AAM4BA",
        caption=(
            "💎 *Telegram Premium*\n\n"
            "• 3 оylik - 170 000\n"
            "• 6 oylik - 220 000\n"
            "• 12 oylik - 390 000\n\n"
            "Выберите действие ниже ⬇️"
        ),
        reply_markup=premium_options_keyboard()
    )


@router.message(F.text == "⭐ Telegram Stars")
async def stars(message: Message):
    users_activity[message.from_user.id] = datetime.now()
    await message.answer_photo(
        photo="AgACAgIAAxkBAAN5aX9HizXNcj5r2ak6qHtoGsCKBnQAApEQaxsvc_hLipQXkfQZE34BAAMCAAN4AAM4BA",
        caption=(
            "⭐ *Telegram Stars*\n\n"
            "• 50 stars — 12 000\n"
            "• 100 stars — 24 000\n\n"
            "Выберите действие ниже ⬇️"
        ),
        reply_markup=stars_options_keyboard()
    )


@router.message(F.text.in_(premium_prices.keys()))
async def buy_premium(message: Message):
    price = premium_prices[message.text]
    users_activity[message.from_user.id] = datetime.now()
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Telegram Premium",
        description=f"Оплата {message.text}",
        payload=f"premium_{message.from_user.id}",
        provider_token=PROVIDER_TOKEN,
        currency="UZS",
        prices=[LabeledPrice(label=message.text, amount=price)]
    )


@router.message(F.text.in_(stars_prices.keys()))
async def buy_stars(message: Message):
    price = stars_prices[message.text]
    users_activity[message.from_user.id] = datetime.now()
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Telegram Stars",
        description=f"Оплата {message.text}",
        payload=f"stars_{message.from_user.id}",
        provider_token=PROVIDER_TOKEN,
        currency="UZS",
        prices=[LabeledPrice(label=message.text, amount=price)]
    )


@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    users_activity[message.from_user.id] = datetime.now()
    orders.append({
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "amount": message.successful_payment.total_amount,
        "currency": message.successful_payment.currency,
        "product": message.successful_payment.invoice_payload
    })
    await message.answer("✅ Оплата прошла успешно! Менеджер свяжется с вами.")
    await bot.send_message(MANAGER_USERNAME, f"💰 Новый заказ от @{message.from_user.username}")


@router.message(F.text == "📩 Написать менеджеру")
async def manager(message: Message):
    await message.answer(f"📩 Менеджер: {MANAGER_USERNAME}")

@router.message(F.text == "⭐ Отзывы")
async def reviews(message: Message):
    await message.answer("⭐ Отзывы:\nВсё быстро и надёжно ✅")

@router.message(F.text == "🛡 Гарантия")
async def guarantee(message: Message):
    await message.answer(
        "🛡 Гарантия:\n"
        "✅ Без входа в аккаунт\n"
        "✅ Безопасно\n"
        "✅ Возврат при проблемах"
    )

@router.message(F.text == "❓ Вопросы")
async def faq(message: Message):
    await message.answer("❓ Вопросы:\nПароль не нужен ❌\nОжидание 1-2 часа ⏱")

@router.message(F.text == "⬅️ Назад")
async def back(message: Message):
    await start(message)


@router.message(F.text == "/orders")
async def admin_orders(message: Message):
    if str(message.from_user.username) != MANAGER_USERNAME.replace("@", ""):
        await message.answer("❌ У вас нет доступа к этой команде.")
        return
    if not orders:
        await message.answer("Заказов пока нет.")
        return
    text = "📋 Заказы:\n"
    for o in orders:
        text += f"- @{o['username']} | {o['product']} | {o['amount']/100} {o['currency']}\n"
    await message.answer(text)



@router.message()
async def auto_start(message: Message):
    users_activity[message.from_user.id] = datetime.now()
    known_texts = [
        "/start", "💎 Telegram Premium", "⭐ Telegram Stars",
        "3 месяца — 170 000", "6 месяцев — 220 000", "12 месяцев — 390 000",
        "50 stars — 12 000", "100 stars — 24 000",
        "📩 Написать менеджеру",
        "⭐ Отзывы", "🛡 Гарантия", "❓ Вопросы", "⬅️ Назад", "/orders"
    ]
    if message.text in known_texts:
        return
    await message.answer("Добро пожаловать 👋\nВыберите товар:", reply_markup=start_keyboard())


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)


    asyncio.create_task(start_inactive_checker(check_interval_hours=1, inactive_hours=24))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())