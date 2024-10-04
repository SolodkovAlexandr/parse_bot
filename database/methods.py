from sqlalchemy import select

from database.models import Channel, async_session


async def set_channel(tg_url, name):
    async with async_session() as session:
        session.add(Channel(tg_url=tg_url, name=name))
        await session.commit()


async def delete_channel(name):
    async with async_session() as session:
        session.delete(Channel(name=name))


async def get_channels():
    async with async_session() as session:
        return await session.scalars(select(Channel))
