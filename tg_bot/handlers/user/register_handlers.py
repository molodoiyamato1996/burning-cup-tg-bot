from aiogram import Dispatcher

from ..user.start import register_handlers_start
from ..user.create_member import register_handlers_create_member


def register_handlers_user(dp: Dispatcher):
    register_handlers_start(dp)
    register_handlers_create_member(dp)
