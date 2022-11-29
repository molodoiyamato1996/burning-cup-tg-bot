from aiogram import Dispatcher

from tg_bot.handlers.team_player import register_handlers_team_player

from .start import register_handlers_start
from .menu import register_handlers_menu
from .rules import register_handlers_menu_rules
from .support import register_handlers_menu_support
from .team import register_handlers_team
from .profile import register_handlers_profile


def register_handlers_player(dp: Dispatcher):
    register_handlers_team_player(dp)
    register_handlers_start(dp)
    register_handlers_menu(dp)
    register_handlers_menu_rules(dp)
    register_handlers_team(dp)
    register_handlers_menu_support(dp)
    register_handlers_profile(dp)
