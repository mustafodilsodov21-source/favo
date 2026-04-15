from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⭐ Купить Stars")],
            [KeyboardButton(text="💰 Мои покупки")]
        ],
        resize_keyboard=True
    )
    return kb