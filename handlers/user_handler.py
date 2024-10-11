from typing import List, Dict

import sqlalchemy.exc
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from database import get_all_channels, set_channel, delete_channel, Channel
from keyboards.simple_kb import create_nav_menu
from lexicon import LEXICON
from utils import FSMChannelState, parse_text_link

router: Router = Router()


# команда старт, дефолтный стейт
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['hello'], reply_markup=create_nav_menu(
        'add_ch', 'del_ch', 'get_ch', 'result'
    ))


# конанда назад из машины состояний
@router.message(F.text == LEXICON['back'], ~StateFilter(default_state))
async def process_to_back(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['cancel'], reply_markup=create_nav_menu(
        'add_ch', 'del_ch', 'get_ch', 'result'
    ))
    await state.clear()


# нажали на кнопку добавить канал, ставим стейт добавления
@router.message(F.text == LEXICON['add_ch'], StateFilter(default_state))
async def process_to_add_channel(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['add_ch_text'],
                         disable_web_page_preview=True,
                         reply_markup=create_nav_menu(
                             'back'
                         ))
    await state.set_state(FSMChannelState.add_channel)


# ожидаем валидного ввода от пользователя
@router.message(StateFilter(FSMChannelState.add_channel),
                (F.text.startswith('https://')))
async def process_add_channel_sent(message: Message, state: FSMContext):
    tg_url, *name = message.text.split()
    if tg_url.startswith('https://t.me/'):
        tg_url = tg_url[13:]

    try:
        await set_channel(tg_url=tg_url, name=' '.join(name))
        await message.answer(text=LEXICON['success_add'], reply_markup=create_nav_menu(
            'add_ch', 'del_ch', 'get_ch', 'result'
        ))
        await state.clear()
    except sqlalchemy.exc.IntegrityError:
        await message.answer(text=LEXICON['not_uniq_name'].format(name))


# ввели некорректный текст
@router.message(StateFilter(FSMChannelState.add_channel))
async def warning_not_channel(message: Message):
    await message.answer(text=LEXICON['not_link'])


# нажали на кнопку удаления канала, ставим стейт удаления
@router.message(F.text == 'Удалить канал', StateFilter(default_state))
async def process_to_del_channel(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['del_ch_text'],
                         reply_markup=create_nav_menu(
                             'back'
                         ))
    await state.set_state(FSMChannelState.del_channel)


@router.message(StateFilter(FSMChannelState.del_channel), F.text.isalnum())
async def process_to_del_channel_sent(message: Message, state: FSMContext):
    # try:
    await delete_channel(name=message.text)
    #     await message.answer(text=LEXICON['success_del'])
    #     await state.clear()
    # except sqlalchemy.exc.InvalidRequestError:
    #     await message.answer(text=LEXICON['channel_not_found'])


@router.message(F.text == LEXICON['get_ch'])
async def process_to_add_channel(message: Message):
    all_channels = [i.name for i in await get_all_channels()]
    if all_channels:
        await message.answer(text='\n'.join(all_channels))
    else:
        await message.answer(text=LEXICON['empty_channel_list'])


@router.message(F.text == LEXICON['result'])
async def process_result(message: Message):
    all_channels: List[Channel.tg_url] = [i.tg_url for i in await get_all_channels()]
    if all_channels:

        parsed_data: Dict[str: Dict] = parse_text_link(all_channels)
        for k, v in parsed_data.items():
            text_to_send = []
            for i in v.values():
                text_to_send.append(' '.join(i))
            await message.answer(text=LEXICON['result_out_text'].format(
                k, len(v.keys()), '\n\n'.join(text_to_send)
            ), disable_web_page_preview=True
            )


    else:
        await message.answer(text=LEXICON['empty_channel_list'])


@router.message(StateFilter(default_state))
async def send_auto_answer(message: Message):
    await message.answer(text=LEXICON['other_text'])
