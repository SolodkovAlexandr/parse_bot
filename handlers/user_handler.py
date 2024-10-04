import sqlalchemy.exc
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from keyboards.simple_kb import create_nav_menu
from lexicon import LEXICON
from utils import FSMChannelState
from database import get_channels, set_channel, delete_channel

router: Router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['hello'], reply_markup=create_nav_menu(
        'add_ch', 'del_ch', 'get_ch', 'result'
    ))


@router.message(F.text == 'Назад', ~StateFilter(default_state))
async def process_to_add_channel(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['cancel'], reply_markup=create_nav_menu(
        'add_ch', 'del_ch', 'get_ch', 'result'
    ))
    await state.clear()


@router.message(F.text == 'Добавить канал', StateFilter(default_state))
async def process_to_add_channel(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['add_ch_text'],
                         disable_web_page_preview=True,
                         reply_markup=create_nav_menu(
                             'back'
                         ))
    await state.set_state(FSMChannelState.add_channel)


@router.message(StateFilter(FSMChannelState.add_channel),
                (F.text.startswith('https://')) | (F.text.startswith('t.me')))
async def process_add_channel_sent(message: Message, state: FSMContext):
    #     func to parse text on url and name for add
    #     if text success -> save to db and clear state
    #     else wait success enter
    print(await state.get_data())
    print(await state.get_state())
    tg_url, name = message.text.split()

    try:
        await set_channel(tg_url=tg_url, name=name)
        await message.answer(text=LEXICON['success_add'], reply_markup=create_nav_menu(
        'add_ch', 'del_ch', 'get_ch', 'result'
        ))
        await state.clear()
    except sqlalchemy.exc.IntegrityError:
        await message.answer(text=LEXICON['not_uniq_name'].format(name))

@router.message(StateFilter(FSMChannelState.add_channel))
async def warning_not_channel(message: Message):
    await message.answer(text=LEXICON['not_link'])

@router.message(F.text == 'Удалить канал', StateFilter(default_state))
async def process_to_add_channel(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['del_ch_text'],
                         reply_markup=create_nav_menu(
                             'del_ch', 'back'
                         ))
    await state.set_state(FSMChannelState.del_channel)


@router.message(F.text == 'Список каналов')
async def process_to_add_channel(message: Message):
    all_channels = [i.name for i in await get_channels()]
    if all_channels:
        await message.answer(text='\n'.join(all_channels))
    else:
        await message.answer(text=LEXICON['empty_Channel_list'])


@router.message(StateFilter(default_state))
async def send_auto_answer(message: Message):
    await message.answer(text=LEXICON['other_text'])
