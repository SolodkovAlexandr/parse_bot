from dataclasses import dataclass

from environs import Env


@dataclass
class TelegramBot:
    token: str
    root: int


@dataclass
class Config:
    tg_bot: TelegramBot


def load_config(path = None) -> Config:

    env: Env = Env()
    env.read_env()
    return Config(
        tg_bot=TelegramBot(
            token=env('BOT_TOKEN'),
            root=env.int('ROOT')
        )
    )
