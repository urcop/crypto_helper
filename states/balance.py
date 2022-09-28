from aiogram.dispatcher.filters.state import StatesGroup, State


class Balance(StatesGroup):
    count = State()
    address = State()
