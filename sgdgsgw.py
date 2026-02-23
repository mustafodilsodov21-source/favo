from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from wsadfsd import mood_keyboard
from data import TOKEN
import asyncio
import logging
import random


bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

quotes = {
    "грустно": [
        "Иногда грусть — это просто усталость души.",
        "Даже самые сильные иногда молча плачут.",
        "Грусть приходит, когда слова заканчиваются."
    ],
    "плохо": [
        "Плохие дни не делают плохую жизнь.",
        "Это состояние пройдёт, как и всё.",
        "Иногда нужно просто переждать."
    ],
    "печально": [
        "Печаль — тень чувств.",
        "Даже тишина иногда кричит.",
        "Сердце знает, но молчит."
    ],
    "тяжело": [
        "Ты держишься сильнее, чем думаешь.",
        "Тяжело — не значит навсегда.",
        "Ты не один в этом."
    ],
    "одиноко": [
        "Одиночество — когда никто не слышит.",
        "Иногда даже среди людей пусто.",
        "Тишина бывает слишком громкой."
    ],
    "пусто": [
        "Пустота тоже чувство.",
        "Когда внутри пусто — просто подожди.",
        "Пустота не вечна."
    ],
    "не по себе": [
        "Иногда не нужно объяснений.",
        "Просто переживи этот момент.",
        "Это чувство пройдёт."
    ],
    "на душе тяжело": [
        "Душа тоже устаёт.",
        "Ты не обязан быть сильным всегда.",
        "Дай себе время."
    ],
    "помолчать": [
        "Иногда молчание — лучший ответ.",
        "Тишина лечит.",
        "Просто будь."
    ]
}


@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "Как ты себя чувствуешь?",
        reply_markup=mood_keyboard()
    )


@router.callback_query()
async def callback_handler(callback: CallbackQuery):
    mood = callback.data
    text = random.choice(quotes[mood])

    await callback.message.answer(text)
    await callback.answer()


async def main():
    dp.include_router(router)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())