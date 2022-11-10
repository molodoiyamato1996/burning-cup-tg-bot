from aiogram.dispatcher.filters.state import StatesGroup, State


class VerifRequestMember(StatesGroup):
    ENTER_RESPONSE = State()
