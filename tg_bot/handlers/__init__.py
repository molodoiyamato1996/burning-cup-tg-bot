from aiogram import Dispatcher


from .admin import register_handlers_admin
from .moderator import register_handlers_moderator
from .captain import register_handlers_captain
from .team_player import register_handlers_team_player
from .player import register_handlers_player
from .member import register_handlers_member
from .user import register_handlers_user


def register_all_handlers(dp: Dispatcher):
    register_handlers_admin(dp)
    register_handlers_moderator(dp)
    register_handlers_captain(dp)
    register_handlers_team_player(dp)
    register_handlers_player(dp)
    register_handlers_member(dp)
    register_handlers_user(dp)
