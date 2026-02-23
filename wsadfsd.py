from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def mood_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="😞 грустно", callback_data="грустно"),
                InlineKeyboardButton(text="😣 плохо", callback_data="плохо")
            ],
            [
                InlineKeyboardButton(text="😔 печально", callback_data="печально"),
                InlineKeyboardButton(text="😖 тяжело", callback_data="тяжело")
            ],
            [
                InlineKeyboardButton(text="😔 одиноко", callback_data="одиноко"),
                InlineKeyboardButton(text="🕳 пусто внутри", callback_data="пусто")
            ],
            [
                InlineKeyboardButton(text="😕 не по себе", callback_data="не по себе"),
                InlineKeyboardButton(text="💔 на душе тяжело", callback_data="на душе тяжело")
            ],
            [
                InlineKeyboardButton(text="🤐 хочу помолчать", callback_data="помолчать")
            ]
        ]
    )