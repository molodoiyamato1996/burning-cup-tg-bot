from aiogram import Dispatcher

from tg_bot.handlers.member.create_player import register_handlers_create_player
from tg_bot.handlers.member.start import register_handlers_start


def register_handlers_member(dp: Dispatcher):
    register_handlers_start(dp)
    register_handlers_create_player(dp)
