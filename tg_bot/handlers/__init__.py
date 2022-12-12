from aiogram import Dispatcher

from .manager import register_handlers_moderator, register_handlers_admin
from .player import register_handlers_player
from .register import register_handlers_register


def register_all_handlers(dp: Dispatcher):
    register_handlers_admin(dp)
    register_handlers_moderator(dp)
    register_handlers_player(dp)
    register_handlers_register(dp)
