from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import __


def start_keyboard(lang):
    result = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(__('Инструкции', src='ru', dest=lang).text),
            KeyboardButton(__('Аренда BiPlexSystems', src='ru', dest=lang).text)
        ],
        [
            KeyboardButton(__('Партнерская структура', src='ru', dest=lang).text),
            KeyboardButton(__('Баланс', src='ru', dest=lang).text),
        ],
        [
            KeyboardButton(__('Наш маркетинг', src='ru', dest=lang).text),
            KeyboardButton(__('Изменить язык', src='ru', dest=lang).text)
        ]
    ], resize_keyboard=True)
    return result
