from aiogram import Dispatcher

from .management import register_handlers_management
from .menu_tournaments import register_handlers_menu_tournaments
from .add_tournament import register_handlers_add_tournament


def register_handlers_tournaments(dp: Dispatcher):
    register_handlers_management(dp)
    register_handlers_add_tournament(dp)
    register_handlers_menu_tournaments(dp)
