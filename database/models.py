from sqlalchemy import String, INT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(40))
    tg_id: Mapped[int] = mapped_column(INT)

    channels: Mapped[list["Channels"]] = relationship("Channels", back_populates="user")

    def __repr__(self) -> str:
        return f"User: id={self.id}, username={self.username}, telegram_id={self.tg_id}"


class Channels(Base):
    __tablename__ = 'channels'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_url: Mapped[str] = mapped_column(String(50))
    channel_name: Mapped[str] = mapped_column(String(25))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False,  )
    user: Mapped["Users"] = relationship("Users", back_populates="channels")
