from aiogram import Router, F
from aiogram.types import Message
from keyboards.admin_kb import admin_kb
from services.notify import users
from config import ADMIN_ID

router = Router()

@router.message(F.text == "👨‍💼 Админ")
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("👨‍💼 Панель", reply_markup=admin_kb())

@router.message(F.text == "📋 Пользователи")
async def users_list(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(f"👥 Пользователей: {len(users)}")

@router.message(F.text == "📢 Рассылка")
async def broadcast(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("✍️ Напиши текст рассылки:")
    router.message.register(send_broadcast, F.text)

async def send_broadcast(message: Message):
    from aiogram import Bot
    from config import TOKEN

    bot = Bot(token=TOKEN)
    for user_id in users:
        try:
            await bot.send_message(user_id, message.text)
        except:
            pass

    await message.answer("✅ Отправлено")

@router.message(F.text == "⬅️ Назад")
async def back(message: Message):
    from keyboards.main_kb import main_kb
    await message.answer("⬅️ Назад", reply_markup=main_kb())