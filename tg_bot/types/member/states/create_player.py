from aiogram.dispatcher.filters.state import StatesGroup, State


class CreatePlayer(StatesGroup):
    ENTER_USERNAME = State()
    ENTER_DISCORD = State()
    ENTER_FASCTCUP = State()
