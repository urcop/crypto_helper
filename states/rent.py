from aiogram.dispatcher.filters.state import StatesGroup, State


class RentState(StatesGroup):
    api_key = State()
    secret_key = State()
    period = State()