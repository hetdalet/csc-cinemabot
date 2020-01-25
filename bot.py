# -*- coding: utf-8 -*-


import os
import sys
import telebot
from sources import kinopoisk


SOURCES = (kinopoisk,)
REPORT = '\n'.join(('{title} ({year})',
                    'Режиссер: {director}',
                    'Жанр: {genre}',
                    'В ролях: {starring}',
                    'Страна: {country}',
                    'Идет: {duration} мин',
                    'Рейтинг: {rating}'))
HELP = (
    '/start\nНачать работу с ботом.',
    '[название_фильма]\nПолучить информацию о фильме. Пример: [Логан].',
    '[test]\nПроверить работоспособность бота.',
    '/help\nПоказать это сообщение.',
)
NONE = '-'
try:
    TOKEN = os.environ['TOKEN']
except KeyError:
    TOKEN = sys.argv[1]

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, что будем смотреть?')


@bot.message_handler(commands=['/find'])
def start_handler(message):
    bot.send_message(message.chat.id, str(message))


@bot.message_handler(commands=['help'])
def start_handler(message):
    for msg in HELP:
        bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    search_string = text.strip('[]')
    results = fetch(search_string)
    if results:
        send_results(chat_id, results)
    else:
        send_not_found(chat_id)


def send_results(chat_id, film_info):
    for inf in film_info:
        inf = {k: v or NONE for k, v in inf.items()}
        text = REPORT.format(**inf)
        if inf['poster'] != NONE:
            bot.send_photo(chat_id=chat_id, photo=inf['poster'], caption=text)
        else:
            bot.send_message(chat_id, text)


def send_not_found(chat_id):
    bot.send_message(chat_id, 'К сожалению, ничего не нашлось:(')


def fetch(search_string):
    info = None
    for source in SOURCES:
        info = source.fetch(search_string)
        if info:
            break
    return info


if __name__ == '__main__':
    bot.polling()
