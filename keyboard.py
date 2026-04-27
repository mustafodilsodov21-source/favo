from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 O'zbek"), KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇬🇧 English")]
    ],
    resize_keyboard=True
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🤖 ChatGPT")],
        [KeyboardButton(text="🧹 Очистить память")],
        [KeyboardButton(text="🌍 Сменить язык")]
    ],
    resize_keyboard=True
)