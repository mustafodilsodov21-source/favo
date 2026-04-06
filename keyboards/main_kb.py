from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💵 USD"), KeyboardButton(text="📊 Курс")],
            [KeyboardButton(text="🔢 Конвертер"), KeyboardButton(text="🔔 Уведомления")],
            [KeyboardButton(text="👨‍💼 Админ")]
        ],
        resize_keyboard=True
    )