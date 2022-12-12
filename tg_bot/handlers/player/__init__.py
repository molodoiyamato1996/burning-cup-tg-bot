from aiogram import Dispatcher

from .menu import register_handlers_menu
from .profile import register_handlers_profile
from .team import register_handlers_team


def register_handlers_player(dp: Dispatcher):
    register_handlers_menu(dp)
    register_handlers_profile(dp)
    register_handlers_team(dp)
