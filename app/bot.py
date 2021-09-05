# -*- coding: utf-8 -*-


import functools
import os
import sys
import time
import telebot
from sources import kinopoisk


SOURCES = (kinopoisk,)
PARSE_MODE = 'Markdown'
REPORT = '\n'.join(('*{title}* ({year})',
                    '*Режиссер*: {director}',
                    '*Жанр*: {genre}',
                    '*В ролях*: {starring}',
                    '*Страна*: {country}',
                    '*Идет*: {duration} мин',
                    '*Рейтинг*: {rating}'))
HI = ('Привет! Чтобы получить информацию о фильме отправь в сообщении '
      'его название. Не обязательно помнить название точно, найдётся всё:)')
HELP = '\n'.join(('Чтобы получить информацию о фильме или сериале, '
                  'отпрвьте сообщение с его названием, или частью названия.\n',
                  'Так же поддерживаются команды',
                  '*/start* — Начать работу с ботом.',
                  '*[test]* — Проверить работоспособность бота.',
                  '*/help* — Показать этo сообщения.'))
INDICATOR = ('Поиск', 'Поиск.', 'Поиск..', 'Поиск...')
FOUND = 'Вот, что нашлось по запросу «*{}*»:'
NOT_FOUND = 'К сожалению, ничего не нашлось:('
PLACEHOLDER = '—'
NONE = '[NONE]'
try:
    TOKEN = os.environ['TOKEN']
except KeyError:
    TOKEN = sys.argv[1]

bot = telebot.TeleBot(TOKEN)
send_message_pm = functools.partial(bot.send_message, parse_mode=PARSE_MODE)
send_photo_pm = functools.partial(bot.send_photo, parse_mode=PARSE_MODE)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    send_message_pm(message.chat.id, HI)


@bot.message_handler(commands=['help'])
def help_handler(message):
    send_message_pm(message.chat.id, HELP)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    search_string = message.text.lower()
    chat_id = message.chat.id

    indicator_msg = bot.send_message(chat_id, INDICATOR[0])
    upd_indicator_msg = functools.partial(
        bot.edit_message_text,
        chat_id=chat_id,
        message_id=indicator_msg.message_id,
        parse_mode=PARSE_MODE
    )
    result = _wait_result(fetch(search_string), upd_indicator_msg, INDICATOR)

    if result:
        upd_indicator_msg(text=FOUND.format(message.text))
        _send_results(chat_id, message.text, result)
    else:
        upd_indicator_msg(text=NOT_FOUND)


def _wait_result(future_result, upd_indicator, indicator):
    ind_len = len(indicator)
    step = 1
    while not future_result.done:
        upd_indicator(text=indicator[step % ind_len])
        step += 1
        time.sleep(0.2)

    return future_result.wait()


def _send_results(chat_id, search_string, film_info):
    for inf in film_info:
        inf['year'] = inf['year'] or PLACEHOLDER
        has_poster = bool(inf['poster'])
        inf = {k: v or NONE for k, v in inf.items()}
        text = REPORT.format(**inf)
        text = '\n'.join(ln for ln in text.split('\n') if NONE not in ln)
        if has_poster:
            send_photo_pm(chat_id=chat_id, photo=inf['poster'], caption=text)
        else:
            send_message_pm(chat_id, text)
    send_message_pm(chat_id, 'Поискать что-нибудь ещё?')


@telebot.util.async_dec()
def fetch(search_string, *args, **kwargs):
    info = None
    for source in SOURCES:
        info = source.fetch(search_string, *args, **kwargs)
        if info:
            break
    return info


if __name__ == '__main__':
    bot.polling()
