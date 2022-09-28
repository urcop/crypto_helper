from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.balance_keyboard import balance_keyboard, balance_callback, accept_input, \
    admin_balance_keyboard_output, admin_balance_keyboard_input
from loader import dp, db, bot, __, change_lang
from states.balance import Balance

balance_state = ''


@dp.message_handler(text=change_lang('Баланс'))
async def balance(message: types.Message):
    bal = await db.get_balance(message.from_user.id)
    lang = await db.language(tg_id=message.from_user.id, take=True)
    text = __(f'Ваш текущий баланс - {bal} USDT', src='ru', dest=lang)
    await message.answer(text.text, reply_markup=balance_keyboard(lang))

@dp.callback_query_handler(balance_callback.filter())
async def balance_actions(call: CallbackQuery):
    lang = await db.language(tg_id=call.from_user.id, take=True)
    global balance_state
    balance_state = call['data'].split(':')[-1]
    await Balance.count.set()
    await call.message.delete()
    text = __('Введите количество USDT', src='ru', dest=lang)
    await call.message.answer(text.text)


@dp.message_handler(state=Balance.count)
async def count_balance(message: types.Message, state: FSMContext):
    global balance_state
    async with state.proxy() as data:
        try:
            bal = await db.get_balance(message.from_user.id)
            lang = await db.language(tg_id=message.from_user.id, take=True)
            data['count'] = int(message.text)
            if balance_state == 'input_balance':
                await message.answer(
                    __(f'Переведите {data["count"]} USDT на адрес:', src='ru',
                       dest=lang).text + '\n<code>THyL3DR36CaksY2yb3VjzY6y7JhGF3RmA3</code>',
                    reply_markup=accept_input)

            elif balance_state == 'output_balance':
                if int(data['count']) <= int(bal):
                    await message.answer(
                        __('Введите адрес USDT, на который хотите вывести баланс', src='ru', dest=lang).text)
                    await Balance.next()
                else:
                    await message.answer(__('Недостаточный баланс! Введите другое число', src='ru', dest=lang).text)
        except ValueError:
            await message.answer(__('Введите число!', src='ru', dest=lang).text)


@dp.callback_query_handler(state=Balance.count)
async def accept_inp(call: CallbackQuery, state: FSMContext):
    lang = await db.language(tg_id=call.from_user.id, take=True)
    async with state.proxy() as data:
        if call['data'].split(':')[-1] == 'yes':
            text = [
                'Заявка на пополнение!',
                f'Пользователь {call.from_user.get_mention(as_html=True)}',
                f'Добавить: {data["count"]} USDT',
            ]
            await bot.send_message('-649646788', "\n".join(text),
                                   reply_markup=admin_balance_keyboard_input(data["count"], call.from_user.id))
            await call.message.delete()
            await call.message.answer(
                __('Ваша заявка отправлена, после рассмотрения администратора вам будет начислен баланс', src='ru',
                   dest=lang).text
            )
            await state.finish()
        else:
            await call.message.delete()
            await state.finish()
            await call.message.answer('Отменено')


@dp.message_handler(state=Balance.address)
async def output_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        lang = await db.language(tg_id=message.from_user.id, take=True)
        data['address'] = message.text
        text = [
            'Заявка на вывод!',
            f'Пользователь {message.from_user.get_mention(as_html=True)}',
            f'Вывести: {data["count"]} USDT',
            f'Адрес: <code>{data["address"]}</code>'
        ]
        await bot.send_message('-649646788', "\n".join(text),
                               reply_markup=admin_balance_keyboard_output(data["count"], message.from_user.id))

        await message.answer(__('Ваша заявка отправлена', src='ru', dest=lang).text)
        await state.finish()
