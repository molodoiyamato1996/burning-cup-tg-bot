from aiogram import Dispatcher

from .team_player import register_handlers_team_player

from tg_bot.handlers.player.start import register_handlers_start
from tg_bot.handlers.player.create_team import register_handlers_create_team
from tg_bot.handlers.player.join_team import register_handlers_join_team
from tg_bot.handlers.player.menu import register_handlers_menu
from tg_bot.handlers.player.set_dicsord import register_handlers_set_discord
from tg_bot.handlers.player.set_fastcup import register_handlers_set_fastcup
from tg_bot.handlers.player.set_username import register_handlers_set_username


def register_handlers_player(dp: Dispatcher):
    register_handlers_team_player(dp)
    register_handlers_start(dp)
    register_handlers_menu(dp)
    register_handlers_create_team(dp)
    register_handlers_join_team(dp)
    register_handlers_set_username(dp)
    register_handlers_set_fastcup(dp)
    register_handlers_set_discord(dp)
