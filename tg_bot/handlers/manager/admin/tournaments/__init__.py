from aiogram import Dispatcher

from .add_tournament import register_handlers_add_tournament
from .menu_tournaments import register_handlers_menu_tournaments
from .set_tournament import register_handlers_set_tournament

from .management import register_handlers_management

from .registration import register_handlers_registration
from .tournament_teams import register_handlers_tournament_teams


def register_handlers_tournament(dp: Dispatcher):
    register_handlers_add_tournament(dp)
    register_handlers_menu_tournaments(dp)
    register_handlers_set_tournament(dp)
    register_handlers_management(dp)
    register_handlers_registration(dp)
    register_handlers_tournament_teams(dp)
