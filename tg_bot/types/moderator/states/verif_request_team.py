from aiogram.dispatcher.filters.state import StatesGroup, State


class VerifRequestTeam(StatesGroup):
    ENTER_COMMENT_REQUEST_TEAM = State()
