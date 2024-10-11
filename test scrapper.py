from snscrape.modules import telegram as tg
from datetime import datetime as dt

a = tg.TelegramChannelScraper(name='smotri_kakoi_text')
data_list = []
# print(a.get_items())
for i in a.get_items():
    print(i.date)
    print(i.content[:100])
    print(i.url)
    print(type(i.json()))
    # print(i.outlinks)
    # print(i.outlinksss)
    break


# for j in a.get_items():
#     if j.date.day == dt.today().day:
#         data_list.append(j)
#     else:
#         break

print(data_list)