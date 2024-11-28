from typing import Dict

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from database.methods import add_user, add_channel, get_users_channels, delete_channel_by_user_id
from keyboards.simple_kb import create_nav_menu
from lexicon import LEXICON
from utils import FSMChannelState, parse_text_link

router: Router = Router()


# команда старт, дефолтный стейт
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    user = await add_user(tg_id=message.from_user.id, username=message.from_user.username)
    await message.answer(text=LEXICON['hello'].format(message.from_user.username), reply_markup=create_nav_menu(
        'add_ch', 'del_ch', 'get_ch', 'result'
    ))


# команда назад из машины состояний
@router.message(F.text == LEXICON['back'], ~StateFilter(default_state))
async def process_to_back_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=LEXICON['cancel'], reply_markup=create_nav_menu(
        'add_ch', 'del_ch', 'get_ch', 'result'
    ))


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

    new_channel = await add_channel(
        user_id=message.from_user.id,
        username=message.from_user.username,
        channel_name=' '.join(name),
        channel_url=tg_url
    )
    if new_channel:
        await message.answer(text=LEXICON['success_add'], reply_markup=create_nav_menu(
            'add_ch', 'del_ch', 'get_ch', 'result'
        ))
        await state.clear()
    else:
        await message.answer(text=LEXICON['not_uniq_name'].format(*name))


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


# успешно удаляем канал
@router.message(StateFilter(FSMChannelState.del_channel), F.text)
async def process_to_del_channel_sent(message: Message, state: FSMContext):
    deleted = await delete_channel_by_user_id(channel_name=message.text, user_id=message.from_user.id)
    if deleted:
        await message.answer(
            text=LEXICON['success_del'],
            reply_markup=create_nav_menu(
                'add_ch', 'del_ch', 'get_ch', 'result'
            )
        )
        await state.clear()
    else:
        await message.answer(text=LEXICON['channel_not_found'])


@router.message(F.text == LEXICON['get_ch'])
async def process_to_get_channels(message: Message):
    user_channels = await get_users_channels(message.from_user.id)
    channels_name = [channel.channel_name for channel in user_channels]
    if channels_name:
        await message.answer(text='\n'.join(channels_name))
    else:
        await message.answer(text=LEXICON['empty_channel_list'])


@router.message(F.text == LEXICON['result'])
async def process_result(message: Message):
    await message.answer(text=LEXICON["waiting"])
    user_channels = await get_users_channels(message.from_user.id)
    channels_url = {channel.channel_name: channel.channel_url for channel in user_channels}
    if channels_url:

        parsed_data: Dict[str: Dict] = parse_text_link(channels_url)
        for name, texts in parsed_data.items():
            text_to_send = []
            for i in texts.values():
                text_to_send.append(' '.join(i))
            await message.answer(text=LEXICON['result_out_text'].format(
                name, len(texts.keys()), '\n\n'.join(text_to_send)
            ), disable_web_page_preview=True
            )

    else:
        await message.answer(text=LEXICON['empty_channel_list'])


@router.message(StateFilter(default_state))
async def send_auto_answer(message: Message):
    await message.answer(text=LEXICON['other_text'])
