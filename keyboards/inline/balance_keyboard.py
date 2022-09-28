from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import __

balance_callback = CallbackData('balance', 'type')
give_balance = CallbackData('balance_adm_inp', 'count', 'telegram_id', 'action')
take_balance = CallbackData('balance_adm_otp', 'count', 'telegram_id', 'action')
accept_callback = CallbackData('accept', 'choice')


def balance_keyboard(lang):
    result = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(__('Пополнить', src='ru', dest=lang).text,
                                 callback_data=balance_callback.new('input_balance')),
            InlineKeyboardButton(__('Вывод', src='ru', dest=lang).text,
                                 callback_data=balance_callback.new('output_balance'))
        ]
    ])
    return result


def admin_balance_keyboard_input(count, telegram_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('Одобрить', callback_data=give_balance.new(str(count), str(telegram_id), 'yes')),
            InlineKeyboardButton('Отклонить', callback_data=give_balance.new(str(count), str(telegram_id), 'no'))
        ]
    ])
    return keyboard


def admin_balance_keyboard_output(count, telegram_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton('Одобрить', callback_data=take_balance.new(str(count), str(telegram_id), 'yes')),
            InlineKeyboardButton('Отклонить', callback_data=take_balance.new(str(count), str(telegram_id), 'no'))
        ]
    ])
    return keyboard


accept_input = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('✔', callback_data=accept_callback.new('yes')),
        InlineKeyboardButton('✖', callback_data=accept_callback.new('cancel')),
    ]
])
