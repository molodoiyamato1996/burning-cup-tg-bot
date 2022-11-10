from aiogram import Dispatcher

from .team import register_handlers_team_menu
from .captain import register_handlers_captain
from .leave_the_team import register_handlers_leave_the_team


def register_handlers_team_player(dp: Dispatcher):
    register_handlers_captain(dp)
    register_handlers_team_menu(dp)
    register_handlers_leave_the_team(dp)
