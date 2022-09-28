import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.default.start_keyboard import start_keyboard
from keyboards.inline.language_keyboard import language_keyboard, language_callback
from loader import dp, __, db
from states.lang import Language

refer = 0
offer_callback = CallbackData('chioce', 'yes')


@dp.message_handler(CommandStart())
async def choice_lang(message: types.Message):
    global refer
    if len(message.text.split(' ')) == 2:
        refer = message.text.split(' ')[1]
    else:
        refer = 0
    await message.answer('Choose language', reply_markup=language_keyboard)
    await Language.lang.set()


@dp.callback_query_handler(language_callback.filter(), state=Language.lang)
async def settings(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['lang'] = call['data'].split(':')[-1]
        text = __("Данная услуга не имеет отношения к компании MinePlex Banking ,не несёт на себе ответственности за \
        дальнейшую деятельность проекта и его существование, лишь даёт возможность, абонентского использования \
        программного обеспечения нашей собственной разработки для автоматизированной торговли на бирже Bibox\
         посредством подключения через Api Key. Принимая данное соглашение вы принимаете ответственность за состояние \
         своих личных средств в случае закрытия проекта MinePlex Banking , \
         токена Plex и самой биржи Bibox.", src='ru', dest=data['lang'])

        await call.message.delete()
        await call.message.answer(text.text, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(__('Я принимаю условия оферты', src='ru', dest=data['lang']).text,
                                     callback_data=offer_callback.new('yes'))
            ]
        ]))


@dp.callback_query_handler(offer_callback.filter(), state=Language.lang)
async def start(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        global refer
        await call.message.delete()
        try:
            await db.add_user(
                tg_id=call.from_user.id,
                fullname=call.from_user.full_name,
                username=call.from_user.username,
                refer_id=int(refer),
                lang=data['lang']
            )
        except asyncpg.exceptions.UniqueViolationError:
            await db.language(call.from_user.id, lang=data['lang'], update=True)

        await state.finish()
        text = __(
            'BiPlexSystems - это полностью автоматизированная система, работающая на бирже Bibox на паре PLEX/USDT.\n\n',
            src='ru',
            dest=data['lang']).text
        chanel = __('Наш телеграм канал - ', src='ru', dest=data["lang"]).text + ' https://t.me/BiPlexSystems'
        await call.message.answer(text + '\n\n' + chanel, reply_markup=start_keyboard(data['lang']))
