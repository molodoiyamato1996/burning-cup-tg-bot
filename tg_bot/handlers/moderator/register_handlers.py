from aiogram import Dispatcher, types

from .verif_request_member import register_handlers_verif_request_member
from .verif_request_team import register_handlers_verif_request_team


def register_handlers_moderator(dp: Dispatcher):
    register_handlers_verif_request_member(dp)
    register_handlers_verif_request_team(dp)
