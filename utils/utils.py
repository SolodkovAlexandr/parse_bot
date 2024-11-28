from datetime import datetime as dt

import snscrape.modules.telegram as tg

from main import logger


def parse_text_link(channels: dict) -> dict:
    data_dict = dict()
    for name, channel_url in channels.items():
        url_text = dict()
        for i, post in enumerate(tg.TelegramChannelScraper(name=channel_url).get_items(), start=1):
            if post.date.day == dt.today().day:
                try:
                    url_text[i] = [post.url[8:].replace('/s/', '/'), post.content[:150]]
                except TypeError as e:
                    logger.warn(f"При парсинге возникла ошибка {e}")
                    continue
            else:
                break
        data_dict[name] = url_text

    return data_dict
