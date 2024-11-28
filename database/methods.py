from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from main import logger
from .base import connection
from .models import Users, Channels


@connection
async def add_user(session, tg_id: int, username: str) -> Optional[Users]:
    try:
        user = await session.scalar(select(Users).filter_by(tg_id=tg_id))

        if not user:
            new_user = Users(tg_id=tg_id, username=username)
            session.add(new_user)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()


@connection
async def add_channel(session,
                      user_id: int,
                      username: str,
                      channel_name: str,
                      channel_url: str) -> Optional[Channels]:
    try:
        user = await session.scalar(select(Users).filter_by(tg_id=user_id))
        if not user:
            logger.error(f"Пользователь с ID {user_id} не найден.")
            await add_user(tg_id=user_id, username=username)

        new_channel = Channels(
            channel_url=channel_url,
            channel_name=channel_name,
            user_id=user_id
        )
        session.add(new_channel)
        await session.commit()
        logger.info(f"Пользователю {user_id} успешно добавлен канал {channel_name}")
        return new_channel
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении канала: {e}")
        await session.rollback()
        return None


@connection
async def get_users_channels(session, user_id: int) -> Optional[List]:
    try:
        result = await session.scalars(select(Channels).filter_by(user_id=user_id))


        if not result:
            logger.info(f"Каналы для пользователя {user_id} не найдены")
            return []

        return result

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении каналов: {e}")
        return []


@connection
async def delete_channel_by_user_id(session: AsyncSession, channel_name: str, user_id: int) -> Optional:
    try:
        result = await session.execute(
            select(Channels).where(Channels.user_id == user_id).where(Channels.channel_name == channel_name))
        channel = result.scalar_one()

        if not channel:
            logger.info(f"Канал {channel_name} не найден у пользователя {user_id}")
            return []
        await session.delete(channel)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении каналов: {e}")
        return []
