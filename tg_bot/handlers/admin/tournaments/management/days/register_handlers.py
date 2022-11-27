from aiogram import Dispatcher

from .add_day import register_handlers_add_day
from .days import register_handlers_menu_days


def register_handlers_days(dp: Dispatcher):
    register_handlers_add_day(dp)
    register_handlers_menu_days(dp)
