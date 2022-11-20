from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup

from tg_bot.types.member.type import MemberType


class MemberKb:
    def __init__(self):
        self.create_player_ib = InlineKeyboardButton('Зарегистрировать аккаунт', callback_data='create_player')

    async def get_create_player_ikb(self) -> InlineKeyboardMarkup:
        register_player_ikb = InlineKeyboardMarkup(row_width=1)

        register_player_ikb.add(self.create_player_ib)

        return register_player_ikb
