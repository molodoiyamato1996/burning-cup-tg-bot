from aiogram.dispatcher.filters.state import StatesGroup, State


class SetUsername(StatesGroup):
    ENTER_NEW_USERNAME = State()
