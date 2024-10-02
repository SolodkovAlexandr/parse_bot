from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

add_channel = KeyboardButton(text="Добавить канал")
del_channel = KeyboardButton(text="Удалить канал")

keyboard = ReplyKeyboardMarkup(keyboard=[[add_channel], [del_channel]], resize_keyboard=True)
