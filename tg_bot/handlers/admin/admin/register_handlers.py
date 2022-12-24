from aiogram import Dispatcher

from tg_bot.handlers.admin.admin.manager.players import register_handlers_player
from .start import register_handlers_start
from tg_bot.handlers.admin.admin.manager.teams import register_handlers_teams
from .tournaments import register_handlers_tournament
from tg_bot.handlers.admin.admin.manager.requests import register_handlers_menu_requests


def register_handlers_admin(dp: Dispatcher):
    register_handlers_start(dp)
    register_handlers_menu_requests(dp)
    register_handlers_tournament(dp)
    register_handlers_teams(dp)
    register_handlers_player(dp)
