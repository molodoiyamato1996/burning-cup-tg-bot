from aiogram import Dispatcher

from .menu_profile import register_handlers_menu_profile
from .set_dicsord import register_handlers_set_discord
from .set_fastcup import register_handlers_set_fastcup
from .set_username import register_handlers_set_username


def register_handlers_profile(dp: Dispatcher):
    register_handlers_menu_profile(dp)
    register_handlers_set_discord(dp)
    register_handlers_set_fastcup(dp)
    register_handlers_set_username(dp)
