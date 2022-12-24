from aiogram import Dispatcher

from .banned import register_handlers_banned
from .admin import register_handlers_moderator, register_handlers_admin
from tg_bot.handlers.user.player import register_handlers_player
from tg_bot.handlers.user.register import register_handlers_register


def register_all_handlers(dp: Dispatcher):
    register_handlers_banned(dp)
    register_handlers_admin(dp)
    register_handlers_moderator(dp)
    register_handlers_player(dp)
    register_handlers_register(dp)
