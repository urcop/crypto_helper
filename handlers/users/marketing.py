from aiogram import types

from loader import dp, db, __, change_lang


@dp.message_handler(text=change_lang('Наш маркетинг'))
async def marketing(message: types.Message):
    lang = await db.language(message.from_user.id, take=True)
    text = [
        __('Первая линия: ', src='ru', dest=lang).text + ' <b>8%</b>',
        __('Вторая линия: ', src='ru', dest=lang).text + ' <b>6%</b>',
        __('Третья линия: ', src='ru', dest=lang).text + ' <b>3%</b>',
        __('Четвертая линия: ', src='ru', dest=lang).text + ' <b>2%</b>',
        __('Пятая линия: ', src='ru', dest=lang).text + ' <b>1%</b>',
    ]
    await message.answer('\n\n'.join(text))
