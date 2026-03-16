from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Главное меню
def start_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="⭐ Telegram Stars")
    kb.button(text="💎 Telegram Premium")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

# Кнопки под Premium
def premium_options_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="3 месяца — 170 000")
    kb.button(text="6 месяцев — 220 000")
    kb.button(text="12 месяцев — 390 000")
    kb.button(text="📩 Написать менеджеру")
    kb.button(text="⭐ Отзывы")
    kb.button(text="🛡 Гарантия")
    kb.button(text="❓ Вопросы")
    kb.button(text="⬅️ Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

# Кнопки под Stars
def stars_options_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="50 stars — 12 000")
    kb.button(text="100 stars — 24 000")
    kb.button(text="📩 Написать менеджеру")
    kb.button(text="⭐ Отзывы")
    kb.button(text="🛡 Гарантия")
    kb.button(text="❓ Вопросы")
    kb.button(text="⬅️ Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)