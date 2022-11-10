from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class PlayerKb:
    def __init__(self):
        self.ib_profile = InlineKeyboardButton('👤 Профиль', callback_data='profile')
        self.ib_team = InlineKeyboardButton('👥 Команда', callback_data='team')
        self.ib_rules = InlineKeyboardButton('📝 Регламент', callback_data='rules')
        self.ib_support = InlineKeyboardButton('🆘 Помощь', callback_data='support')

        self.ib_back_to_menu = InlineKeyboardButton('Вернуться', callback_data='back_to_menu')

        self.ib_create_team =  InlineKeyboardButton('👥 Создать команду', callback_data='team?create_team')
        self.ib_join_team = InlineKeyboardButton('Присоединиться к команде', callback_data='join_team')

    async def get_team_player_ikb(self, is_captain: bool = False, team_id: int = None, is_tool_park: bool = None) -> InlineKeyboardMarkup:
        team_ikb = InlineKeyboardMarkup(row_width=1)

        composition = InlineKeyboardButton('Состав', callback_data='team_composition')
        team_ikb.add(composition)

        if is_tool_park:
            return team_ikb

        if is_captain:
            invite_code = InlineKeyboardButton('Код приглашения', callback_data=f'team_invite_code?team_id={team_id}')
            disband_team = InlineKeyboardButton('Расформировать команду', callback_data=f'disband_team?team_id={team_id}')

            team_ikb.add(invite_code).add(disband_team)

        if not is_captain:
            leave_the_team_ib = InlineKeyboardButton('Покинуть команду', callback_data='leave_the_team')
            team_ikb.add(leave_the_team_ib)

        participate = InlineKeyboardButton('🔥 Принять участие', callback_data='participate')
        team_ikb.add(participate)
        team_ikb.add(self.ib_back_to_menu)

        return team_ikb

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

        ikb_menu_menu.add(self.ib_profile).insert(self.ib_team).insert(self.ib_rules).insert(self.ib_support).add(self.ib_back_to_menu)

        return ikb_menu_menu

    async def get_team_ikb(self) -> InlineKeyboardMarkup:
        team_ikb = InlineKeyboardMarkup(row_width=2)

        team_ikb.insert(self.ib_create_team).insert(self.ib_join_team).insert(self.ib_back_to_menu)

        return team_ikb

