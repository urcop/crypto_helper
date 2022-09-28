from aiogram import types

from loader import dp, db, __, change_lang


@dp.message_handler(text=change_lang('Инструкции'))
async def instructions(message: types.Message):
    lang = await db.language(message.from_user.id, take=True)
    text = [
        f'<a href="https://youtube.com/">{__("Презентация BiPlexSystems", src="ru", dest=lang).text}</a>',
        f'<a href="https://youtube.com/">{__("Регистрация на бирже Bibox", src="ru", dest=lang).text}</a>',
        f'<a href="https://youtube.com/">{__("Создание api key на Bibox", src="ru", dest=lang).text}</a>',
        f'<a href="https://youtube.com/">{__("Обзор ТГ бота BiPlexSystems", src="ru", dest=lang).text}</a>',
    ]
    await message.answer('\n\n'.join(text), disable_web_page_preview=True)
