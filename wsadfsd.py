from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Регистрация"),
         KeyboardButton(text="🔐 Вход")],
        [KeyboardButton(text="👤 Профиль"),
         KeyboardButton(text="🚪 Выход")]
    ],
    resize_keyboard=True
)