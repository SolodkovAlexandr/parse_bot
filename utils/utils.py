from datetime import datetime as dt

import snscrape.modules.telegram as tg


def parse_text_link(channels: list) -> dict:
    data_dict = dict()
    for i in channels:
        url_text = dict()
        for k, j in enumerate(tg.TelegramChannelScraper(name=i).get_items(), start=1):
            if j.date.day == dt.today().day:
                try:
                    url_text[k] = [j.url[8:].replace('/s/', '/'), j.content[:150]]
                except TypeError:
                    continue
            else:
                break
        data_dict[i] = url_text

    return data_dict
