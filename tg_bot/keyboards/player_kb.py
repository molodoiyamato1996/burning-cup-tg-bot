from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class PlayerKb:
    def __init__(self):
        self.ib_profile = InlineKeyboardButton('👤 Профиль', callback_data='profile')
        self.ib_team = InlineKeyboardButton('👥 Команда', callback_data='team')
        self.ib_rules = InlineKeyboardButton('📝 Регламент', callback_data='rules')
        self.ib_support = InlineKeyboardButton('🆘 Помощь', callback_data='support')

        self.ib_back_to_menu = InlineKeyboardButton('Вернуться', callback_data='back_to_menu')

        self.ib_create_team = InlineKeyboardButton('👥 Создать команду', callback_data='team?create_team')
        self.ib_join_team = InlineKeyboardButton('Присоединиться к команде', callback_data='join_team')

    async def get_profile_ikb(self) -> InlineKeyboardMarkup:
        profile_ikb = InlineKeyboardMarkup(row_width=1)

        profile_ibs = [
            InlineKeyboardButton('👤 Изменить псевдоним', callback_data='set_username'),
            InlineKeyboardButton('🏆 Изменить фасткап', callback_data='set_fastcup'),
            InlineKeyboardButton('📞 Изменить дискорд', callback_data='set_discord')
        ]

        profile_ikb.add(*profile_ibs)

        profile_ikb.add(self.ib_back_to_menu)

        return profile_ikb

    def get_back_to_menu_ikb(self) -> InlineKeyboardMarkup:
        back_to_menu_ikb = InlineKeyboardMarkup(row_width=1)

        back_to_menu_ikb.add(self.ib_back_to_menu)

        return back_to_menu_ikb

    async def get_menu_ikb(self) -> InlineKeyboardMarkup:
        ikb_menu_menu = InlineKeyboardMarkup(row_width=2)

        ikb_menu_menu.add(self.ib_profile).insert(self.ib_team).insert(self.ib_rules).insert(self.ib_support)

        return ikb_menu_menu

    async def get_team_ikb(self) -> InlineKeyboardMarkup:
        team_ikb = InlineKeyboardMarkup(row_width=2)

        team_ikb.insert(self.ib_create_team).insert(self.ib_join_team).insert(self.ib_back_to_menu)

        return team_ikb

