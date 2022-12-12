from aiogram import Dispatcher

# from .players import register_handlers_players
from .start import register_handlers_start
from .teams import register_handlers_teams
from .tournaments import register_handlers_tournaments


def register_handlers_admin(dp: Dispatcher):
    register_handlers_start(dp)
    register_handlers_tournaments(dp)
    register_handlers_teams(dp)
    # register_handlers_players(dp)
