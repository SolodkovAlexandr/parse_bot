from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon import LEXICON


def create_nav_menu(*buttons) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(
        *[KeyboardButton(text=LEXICON[button] if button in LEXICON else button)
          for button in buttons], width=2
    )

    return kb_builder.as_markup(resize_keyboard=True)
