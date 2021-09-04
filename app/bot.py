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
    text = message.text.lower()
    chat_id = message.chat.id

    indicator_msg = bot.send_message(message.chat.id, INDICATOR[0])
    future_results = fetch(text)
    edit_args = {'chat_id': chat_id,
                 'message_id': indicator_msg.message_id,
                 'parse_mode': PARSE_MODE}
    ind_len = len(INDICATOR)
    step = 1
    while not future_results.done:
        edit_args['text'] = INDICATOR[step % ind_len]
        bot.edit_message_text(**edit_args)
        step += 1
        time.sleep(0.2)

    results = future_results.wait()
    if results:
        edit_args['text'] = FOUND.format(message.text)
        bot.edit_message_text(**edit_args)
        send_results(chat_id, message.text, results)
    else:
        edit_args['text'] = NOT_FOUND
        bot.edit_message_text(**edit_args)


def send_results(chat_id, search_string, film_info):
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
