from aiogram import Dispatcher

from .create_team import register_handlers_create_team
from .join_team import register_handlers_join_team
from .menu_team import register_handlers_menu_team


def register_handlers_team(dp: Dispatcher):
    register_handlers_create_team(dp)
    register_handlers_join_team(dp)
    register_handlers_menu_team(dp)
