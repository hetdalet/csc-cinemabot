# -*- coding: utf-8 -*-

import unittest.mock
import pytest
import app.bot


class FutureObjectMock:
    def __init__(self, result, count=10):
        self._result = result
        self._max_count = count
        self._count = 0

    @property
    def done(self):
        if self._count < self._max_count:
            self._count += 1
            return False
        return True

    def wait(self):
        return self._result


class BotMock:
    def __init__(self, init_msg_id=1):
        self.edit_message_text = unittest.mock.Mock()
        self._message_id = init_msg_id

    def send_message(self, chat_id, text, **kwargs):
        message = unittest.mock.Mock(
            chat=unittest.mock.Mock(id=chat_id),
            text=text,
            message_id=self._message_id
        )
        self._message_id += 1
        return message


def get_message_mock(attrs):
    message = unittest.mock.Mock(
        chat=unittest.mock.Mock(id=attrs['chat_id']),
        text=attrs['text'],
        message_id=attrs['message_id']
    )
    return message


@pytest.fixture()
def setup_text_handler(monkeypatch):
    chat_id = 1
    search_msg_id = 1
    search_string = 'Plan 9'
    search_msg = get_message_mock({
        'chat_id': chat_id,
        'message_id': search_msg_id,
        'text': search_string
    })
    indicator_msg_id = search_msg_id + 1
    bot_mock = unittest.mock.Mock(wraps=BotMock(init_msg_id=indicator_msg_id))
    monkeypatch.setattr(app.bot, 'bot', bot_mock)
    monkeypatch.setattr(app.bot, '_send_results', unittest.mock.Mock())

    expected_edit_message_text_calls = [
        unittest.mock.call(
            chat_id=chat_id,
            message_id=indicator_msg_id,
            parse_mode=app.bot.PARSE_MODE,
            text=app.bot.INDICATOR[i]
        )
        for i in [1, 2, 3, 0, 1, 2, 3, 0, 1, 2]
    ]
    expected = {
        'send_message_call': unittest.mock.call(chat_id, app.bot.INDICATOR[0]),
        'fetch_call': unittest.mock.call(search_msg.text.lower()),
        'edit_message_text_calls': expected_edit_message_text_calls
    }
    return search_msg, indicator_msg_id, expected


@pytest.fixture()
def setup_text_handler_found(monkeypatch, setup_text_handler):
    message, indicator_msg_id, expected = setup_text_handler
    search_result = 'RESULT'

    monkeypatch.setattr(app.bot, 'fetch', unittest.mock.Mock(return_value=FutureObjectMock(search_result)))

    expected['edit_message_text_calls'].append(
        unittest.mock.call(
            chat_id=message.chat.id,
            message_id=indicator_msg_id,
            parse_mode=app.bot.PARSE_MODE,
            text=app.bot.FOUND.format(message.text)
        )
    )
    expected['send_results_call'] = unittest.mock.call(
        message.chat.id,
        search_result
    )
    return message, expected


def test_text_handler_found(setup_text_handler_found):
    message, expected = setup_text_handler_found
    app.bot.text_handler(message)

    assert app.bot.bot.send_message.call_args == expected['send_message_call']
    assert app.bot.fetch.call_args == expected['fetch_call']
    assert app.bot.bot.edit_message_text.call_args_list == expected['edit_message_text_calls']
    assert app.bot._send_results.call_args == expected['send_results_call']


@pytest.fixture()
def setup_text_handler_not_found(monkeypatch, setup_text_handler):
    message, indicator_msg_id, expected = setup_text_handler
    search_result = None

    monkeypatch.setattr(app.bot, 'fetch', unittest.mock.Mock(return_value=FutureObjectMock(search_result)))

    expected['edit_message_text_calls'].append(
        unittest.mock.call(
            chat_id=message.chat.id,
            message_id=indicator_msg_id,
            parse_mode=app.bot.PARSE_MODE,
            text=app.bot.NOT_FOUND
        )
    )
    expected['send_results_call_count'] = 0
    return message, expected


def test_text_handler_not_found(setup_text_handler_not_found):
    message, expected = setup_text_handler_not_found
    app.bot.text_handler(message)

    assert app.bot.bot.send_message.call_args == expected['send_message_call']
    assert app.bot.fetch.call_args == expected['fetch_call']
    assert app.bot.bot.edit_message_text.call_args_list == expected['edit_message_text_calls']
    assert app.bot._send_results.call_count == expected['send_results_call_count']
