from aiogram import Dispatcher

from .start import register_handlers_start
from .matches import register_handlers_matches
from .registration import register_handlers_registration
from .games import register_handlers_games
from .teams import register_handlers_teams


def register_handlers_admin(dp: Dispatcher):
    register_handlers_start(dp)
    register_handlers_matches(dp)
    register_handlers_registration(dp)
    register_handlers_teams(dp)
    register_handlers_games(dp)
