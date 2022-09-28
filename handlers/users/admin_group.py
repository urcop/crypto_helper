from aiogram.types import CallbackQuery

from keyboards.inline.balance_keyboard import give_balance, take_balance
from loader import dp, db, bot, __


@dp.callback_query_handler(give_balance.filter())
async def accept_action_balance(call: CallbackQuery):
    data = call['data'].split(':')
    count = int(data[1])
    telegram_id = int(data[2])
    action = data[3]
    lang = await db.language(telegram_id, take=True)
    if action == 'yes':
        await db.balance(telegram_id, count, give=True)
        await call.message.delete_reply_markup()
        await bot.send_message(telegram_id, __('Ваша заявка одобрена', src='ru', dest=lang).text)
    elif action == 'no':
        await call.message.delete_reply_markup()
        await bot.send_message(telegram_id, __('Ваша заявка отклонена', src='ru', dest=lang).text)


@dp.callback_query_handler(take_balance.filter())
async def accept_action_balance(call: CallbackQuery):
    data = call['data'].split(':')
    count = int(data[1])
    telegram_id = int(data[2])
    action = data[3]
    lang = await db.language(telegram_id, take=True)
    if action == 'yes':
        await db.balance(telegram_id, count, take=True)
        await call.message.delete_reply_markup()
        await bot.send_message(telegram_id, __('Ваша заявка одобрена', src='ru', dest=lang).text)
    elif action == 'no':
        await call.message.delete_reply_markup()
        await bot.send_message(telegram_id, __('Ваша заявка отклонена', src='ru', dest=lang).text)
