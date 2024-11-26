from sqlalchemy import select

from database.models import Channel, async_session


async def set_channel(tg_url, name):
    async with async_session() as session:
        new_channel = Channel(tg_url=tg_url, name=name)
        session.add(new_channel)
        await session.commit()


async def delete_channel(name):
    async with async_session() as session:
        to_delete = await session.execute(select(Channel).where(Channel.name == name))
        session.delete(to_delete)
        await session.commit()


async def get_all_channels():
    async with async_session() as session:
        return await session.scalars(select(Channel))
