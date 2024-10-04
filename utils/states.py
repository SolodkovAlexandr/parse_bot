from aiogram.filters.state import State, StatesGroup


class FSMChannelState(StatesGroup):
    add_channel = State()
    del_channel = State()
