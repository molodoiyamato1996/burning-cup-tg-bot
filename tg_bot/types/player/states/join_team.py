from aiogram.dispatcher.filters.state import StatesGroup, State


class JoinTeam(StatesGroup):
    ENTER_INVITE_CODE = State()
