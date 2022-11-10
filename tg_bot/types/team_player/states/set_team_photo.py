from aiogram.dispatcher.filters.state import StatesGroup, State


class SetTeamPhoto(StatesGroup):
    SEND_NEW_TEAM_PHOTO = State()
