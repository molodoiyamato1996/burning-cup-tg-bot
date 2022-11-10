from aiogram import Dispatcher

from .participate import register_handlers_participate
from .disband_team import register_handlers_dispand_team
from .generate_invite_code import register_handlers_generate_invite_code
from .kick_player import register_handlers_kick_player
from .set_team_name import register_handlers_set_team_name
from .set_team_photo import register_handlers_set_team_photo


def register_handlers_captain(dp: Dispatcher):
    register_handlers_participate(dp)
    register_handlers_set_team_name(dp)
    register_handlers_set_team_photo(dp)
    register_handlers_dispand_team(dp)
    register_handlers_generate_invite_code(dp)
    register_handlers_kick_player(dp)
