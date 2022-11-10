from aiogram.dispatcher.filters.state import StatesGroup, State


class SetDiscord(StatesGroup):
    ENTER_NEW_DISCORD = State()
