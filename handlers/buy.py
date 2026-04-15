from aiogram import types
from database import add_order, get_orders

PRICE_PER_STAR = 200


async def buy_handler(message: types.Message):
    await message.answer("Напиши сколько Stars хочешь купить:")


async def process_amount(message: types.Message):
    try:
        amount = int(message.text)
        price = amount * PRICE_PER_STAR

        add_order(
            user_id=message.from_user.id,
            username=message.from_user.username,
            amount=amount,
            price=price
        )

        await message.answer(
            f"✅ Заказ оформлен!\n"
            f"⭐ Stars: {amount}\n"
            f"💰 Цена: {price} сум"
        )

    except:
        await message.answer("❌ Введи число!")


async def my_orders(message: types.Message):
    orders = get_orders()

    if not orders:
        await message.answer("У тебя пока нет покупок")
        return

    text = "📦 Покупки:\n\n"
    for o in orders:
        text += f"ID:{o[0]} | ⭐{o[3]} | 💰{o[4]}\n"

    await message.answer(text)