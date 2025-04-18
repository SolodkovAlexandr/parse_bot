LEXICON: dict[str, str] = {
    'add_ch': 'Добавить канал',
    'del_ch': 'Удалить канал',
    'get_ch': 'Список каналов',
    'back': 'Назад',
    'back_message': 'Вы вернулись в главное меню',

    'result': 'Получить результат',
    'result_message': 'Вы можете выбрать какую информацию получить:\n\n'
                      '- Получить всю информацию\n'
                      '- Получить информацию за выбранный день\n'
                      '- Получить информацию из выбранных каналов\n',
    'get_all_result': 'Получить всю информацию',
    'select_day': 'Выбрать день/дни',
    'select_ch': 'Выбрать каналы',

    'hello': 'Привет {}!\n\nЯ умею собирать информацию о постах из каналов📊\n'
             'Ты можешь создать свой список интересующих каналов, а также редактировать его.\n'
             'В ответ на запрос я пришлю тебе краткую сводку по каждому посту в каждом из каналов созданного списка',
    'add_ch_text': 'Для добавления канала необходимо прислать ссылку на канал и его название. Пример формата: '
                   'https://t.me/smotri_kakoi_text Копилка текстов',
    'del_ch_text': 'Для удаления канала нужно прислать название канала из списка доступных',
    'cancel': 'Вы прервали процедуру',
    'other_text': 'Я понимаю только команды из меню',
    'success_add': 'Канал успешно добавлен',
    'success_del': 'Канал успешно удалён',
    'not_link': 'Ошибка, нужно ввести как в примере',
    'empty_channel_list': 'Пока список каналов пустой',
    'not_uniq_name': 'Имя канала должно быть уникальным, канал с именем {} уже есть в базе',
    'channel_not_found': 'Канал с таким именем отсутствует в базе',
    'result_out_text': 'В канале <b>{}</b> количество постов за сегодня {}:\n\n{}',
    'waiting': 'Сбор информации по каналом может занять время'
}
