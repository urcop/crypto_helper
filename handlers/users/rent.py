import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.rent_cancel import cancel_button
from keyboards.default.start_keyboard import start_keyboard
from keyboards.inline.rent_keyboard import rent_keyboard, rent_callback
from loader import dp, db, bot, change_lang, __
from states.rent import RentState


def rent_cost(rent):
    if rent == 'rent1':
        return 30
    elif rent == 'rent2':
        return 55
    elif rent == 'rent3':
        return 75
    elif rent == 'rent13':
        return 150


@dp.message_handler(text=change_lang('Назад'), state=RentState.all_states)
async def cancel_request(message: types.Message, state: FSMContext):
    lang = await db.language(message.from_user.id, take=True)
    await state.finish()
    await message.answer(__('Отмена', src='ru', dest=lang).text, reply_markup=start_keyboard(lang))


@dp.message_handler(text=change_lang('Аренда BiPlexSystems'))
async def enter_api(message: types.Message):
    lang = await db.language(message.from_user.id, take=True)
    await message.answer(__('Вставьте ваш api key', src='ru', dest=lang).text, reply_markup=cancel_button)
    await RentState.api_key.set()


@dp.message_handler(state=RentState.api_key)
async def enter_secret_key(message: types.Message, state: FSMContext):
    lang = await db.language(message.from_user.id, take=True)
    async with state.proxy() as data:
        try:
            data['api_key'] = str(message.text)
            await message.answer(__('Вставьте ваш secret key', src='ru', dest=lang).text, reply_markup=cancel_button)
            await RentState.next()
        except Exception as e:
            logging.info(e)
            await state.finish()


@dp.message_handler(state=RentState.secret_key)
async def enter_secret_key(message: types.Message, state: FSMContext):
    lang = await db.language(message.from_user.id, take=True)
    async with state.proxy() as data:
        try:
            data['secret_key'] = str(message.text)
            await RentState.next()
            await message.answer(
                __('Успешно!', src='ru', dest=lang).text + '\n' + __('Выберите план:', src='ru', dest=lang).text,
                reply_markup=rent_keyboard(lang))
        except Exception as e:
            logging.info(e)
            await state.finish()


@dp.callback_query_handler(rent_callback.filter(), state=RentState.period)
async def rent_choice(call: CallbackQuery, state: FSMContext):
    lang = await db.language(call.from_user.id, take=True)
    async with state.proxy() as data:
        period = call['data'].split(':')[1]
        cost = rent_cost(period)
        data['period'] = period
        user = await db.select_user(tg_id=call.from_user.id)
        if int(user['balance']) >= cost:
            try:
                await db.balance(call.from_user.id, cost, take=True)
                await call.message.delete()

                req_data = data.as_dict()
                text = [
                    'Заявка на подписку!',
                    f'Пользователь - {call.from_user.get_mention(as_html=True)}',
                    f'Api-key: <code>{req_data["api_key"]}</code>',
                    f'Secret-key: <code>{req_data["secret_key"]}</code>',
                    f'Срок: {req_data["period"][4::]} мес',
                ]
                await bot.send_message('-649646788', text='\n'.join(text))
                await call.message.answer(__('Ваша заявка на получение подписки отправлена, скоро с вами свяжется '
                                             'модератор', src='ru', dest=lang).text, reply_markup=start_keyboard(lang))
                await call.message.answer(
                    __(f'Отправляй ссылку своим друзьям и партнерам, зарабатывай вместе с нами https://t.me/BiPlexSystems_bot?start={call.from_user.id}',
                       src='ru',
                       dest=lang).text)

                lvls = {
                    "lvl4": 0.01,
                    "lvl3": 0.02,
                    "lvl2": 0.03,
                    "lvl1": 0.06,
                    "lvl0": 0.08
                }
                referer = await db.view_5_lvl(call.from_user.id)
                for i in range(0, 5):
                    await db.balance(referer[i], cost * lvls[f"lvl{i}"], give=True)
                    await db.balance(referer[i], cost * lvls[f"lvl{i}"], earn=True)

                await state.finish()
            except Exception as e:
                logging.info(e)
        else:
            await call.message.delete()
            await call.message.answer(
                __('У вас недостаточно USDT, пополнить можно во вкладке "Баланс"', src='ru', dest=lang).text,
                reply_markup=start_keyboard(lang))
            await state.finish()
