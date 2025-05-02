from aiogram.filters import BaseFilter

from aiogram.types import Message


class IsValidChannel(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict:
        tg_url, *name = message.text.split(maxsplit=1)
        if tg_url.startswith('https://t.me/') and name:
            return {'channel': [tg_url[13:], name[0]]}

        return False
