from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_button = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton('Назад')
    ]
], resize_keyboard=True)
