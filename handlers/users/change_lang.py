from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.default.start_keyboard import start_keyboard
from keyboards.inline.language_keyboard import language_keyboard, language_callback
from loader import dp, db, __


@dp.message_handler(text=['Изменить язык', 'Change the language', 'Changer la langue', 'Ganti basa', 'Ändere die Sprache', 'تغيير اللغة', 'Змінити мову'])
async def change_lang(message: types.Message):
    lang = await db.language(message.from_user.id, take=True)
    await message.answer(__('Выберите язык', src='ru', dest=lang).text, reply_markup=language_keyboard)


@dp.callback_query_handler(language_callback.filter())
async def language(call: CallbackQuery):
    await call.message.delete()
    lang = call['data'].split(':')[-1]
    await db.language(call.from_user.id, lang=lang, update=True)
    await call.message.answer(__('Успешно!', src='ru', dest=lang).text, reply_markup=start_keyboard(lang))
