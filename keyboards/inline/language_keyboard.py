from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

language_callback = CallbackData('lang', 'choice')

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton('🇺🇸 English', callback_data=language_callback.new('en')),
    ],
    [
        InlineKeyboardButton('🇷🇺 Русский', callback_data=language_callback.new('ru'))
    ],
    [
        InlineKeyboardButton('🇫🇷 Français', callback_data=language_callback.new('fr')),
    ],
    [
        InlineKeyboardButton('🇪🇸 Español', callback_data=language_callback.new('su')),
    ],
    [
        InlineKeyboardButton('🇩🇪 Deutsch', callback_data=language_callback.new('de')),
    ],
    [
        InlineKeyboardButton('🇦🇪 العربية', callback_data=language_callback.new('ar')),
    ],
    [
        InlineKeyboardButton('🇺🇦 Український', callback_data=language_callback.new('uk')),
    ]
], row_width=1)

