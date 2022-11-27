from aiogram import Dispatcher

from tg_bot.handlers.team_player import register_handlers_team_player

from .start import register_handlers_start
from .menu import register_handlers_menu
from .menu_rules import register_handlers_menu_rules
from .menu_support import register_handlers_menu_support
from .menu_team import register_handlers_menu_team
from .menu_profile import register_handlers_menu_profile


def register_handlers_player(dp: Dispatcher):
    register_handlers_team_player(dp)
    register_handlers_start(dp)
    register_handlers_menu(dp)
    register_handlers_menu_rules(dp)
    register_handlers_menu_team(dp)
    register_handlers_menu_support(dp)
    register_handlers_menu_profile(dp)
