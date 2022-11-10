from aiogram.dispatcher.filters.state import StatesGroup, State


class ResponseRequestStudent(StatesGroup):
    ENTER_ANSWER = State()
