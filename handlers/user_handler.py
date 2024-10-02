from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from database.methods import set_channel, delete_channel
from keyboards.simple_kb import keyboard

router: Router = Router()

@router.message(CommandStart)
async def process_start_command(message: Message):
    await message.answer('Hello, bro! What do you want?', reply_markup=keyboard)

@router.message(F.text == 'Добавить канал')
async def pocess_to_add_channel(message: Message):
    await message.answer(text='Введи ссылку на канал')
    set_channel()
