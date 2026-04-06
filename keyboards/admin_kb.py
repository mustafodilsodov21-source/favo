from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def admin_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Пользователи")],
            [KeyboardButton(text="📢 Рассылка")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )