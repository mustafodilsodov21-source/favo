from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Dispatcher, Bot, Router

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from data import TOKEN


import logging
import asyncio



bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
print(TOKEN)


class RegisterUser(StatesGroup):
    name = State()
    phone = State()
    email = State()




@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer(
        text='What is your name?',
    )
    await state.set_state(RegisterUser.name)


@router.message(RegisterUser.name)
async def name_function(message: Message, state: FSMContext):
    user_name = message.text
    await state.update_data(name=user_name)
    await message.answer(
        text='What is your phone: ',
    )
    await state.set_state(RegisterUser.phone)


@router.message(RegisterUser.phone)
async def phone_function(message: Message, state: FSMContext):
    user_phone = message.text
    await state.update_data(phone=user_phone)
    await message.answer(
        text='What is your email: ',
    )
    await state.set_state(RegisterUser.email)


@router.message(RegisterUser.email)
async def email_function(message: Message, state: FSMContext):
    user_email = message.text
    await state.update_data(email=user_email)
    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    msg = f"""
    Your data:

    name: {name}
    phone: {phone}
    email: {email}
    """
    await message.answer(
        text=msg,
    )
    await state.clear()


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())