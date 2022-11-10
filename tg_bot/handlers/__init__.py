from aiogram import Dispatcher

from .admin.register_handlers import register_handlers_admin
from .member.register_handlers import register_handlers_member
from .player.register_handlers import register_handlers_player
from .moderator.register_handlers import register_handlers_moderator
from .user.register_handlers import register_handlers_user


def register_all_handlers(dp: Dispatcher):
    register_handlers_admin(dp)
    register_handlers_moderator(dp)
    register_handlers_player(dp)
    register_handlers_member(dp)
    register_handlers_user(dp)
