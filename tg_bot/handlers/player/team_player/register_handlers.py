from aiogram import Dispatcher

from .menu_team import register_handlers_menu_team
from .team_composition import register_handlers_team_composition
from .captain import register_handlers_captain
from .leave_the_team import register_handlers_leave_the_team


def register_handlers_team_player(dp: Dispatcher):
    register_handlers_captain(dp)
    register_handlers_team_composition(dp)
    register_handlers_menu_team(dp)
    register_handlers_leave_the_team(dp)
