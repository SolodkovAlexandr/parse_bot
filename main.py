import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from configs.config import Config, load_config
from database.base import create_table
from handlers import user_handler

logger = logging.getLogger(__name__)
commands = [BotCommand(command="start", description="Старт бота")]


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    config: Config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(user_handler.router)

    try:
        await create_table()
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands, BotCommandScopeDefault())
        await bot.send_message(chat_id=config.tg_bot.root, text='Парсинг бот запущен')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
