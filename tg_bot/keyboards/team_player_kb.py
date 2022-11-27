from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class TeamPLayerKb:
    def __init__(self) -> None:
        self.ib_back_to_team = InlineKeyboardButton(text='Вернуться', callback_data='back_to_team')

        self.ib_participate = InlineKeyboardButton('Принять участие', callback_data='participate')

    async def get_participate_ikb(self) -> InlineKeyboardMarkup:
        participate_ikb = InlineKeyboardMarkup(row_width=1)

        participate_ikb.add(self.ib_participate)

        return participate_ikb

    @staticmethod
    async def get_fail_participate_ikb(team_id: int) -> InlineKeyboardMarkup:
        set_team_ikb = InlineKeyboardMarkup(row_width=1)

        ib_repeated_request = InlineKeyboardButton('Повторная заявка', callback_data='participate')
        ib_set_team_name = InlineKeyboardButton('Изменить название', callback_data=f'set_team_name?team_id={team_id}')
        ib_set_team_photo = InlineKeyboardButton('Изменить фото', callback_data=f'set_team_photo?team_id={team_id}')
        set_team_ikb.add(ib_set_team_name).add(ib_set_team_photo).add(ib_repeated_request)

        return set_team_ikb

    async def get_back_to_team_ikb(self) -> InlineKeyboardMarkup:
        back_to_team_ikb = InlineKeyboardMarkup(row_width=1)

        back_to_team_ikb.add(self.ib_back_to_team)

        return back_to_team_ikb

    @staticmethod
    async def get_confirm_participate_ikb() -> InlineKeyboardMarkup:
        participate_ikb = InlineKeyboardMarkup(row_width=2)

        yes = InlineKeyboardButton('Да', callback_data='confirm_participate')
        no = InlineKeyboardButton('Нет', callback_data='back_to_team')

        participate_ikb.insert(yes).insert(no)

        return participate_ikb

    @staticmethod
    async def get_confirm_kick_team_player_ikb(player_id: int) -> InlineKeyboardMarkup:
        confirm_kick_team_player_ikb = InlineKeyboardMarkup(row_width=2)

        yes = InlineKeyboardButton('Да', callback_data=f'confirm_kick_team_player?player_id={player_id}')
        no = InlineKeyboardButton('Нет', callback_data=f'team_composition')

        confirm_kick_team_player_ikb.add(yes).insert(no)

        return confirm_kick_team_player_ikb

    @staticmethod
    async def get_confirm_leave_the_team_ikb() -> InlineKeyboardMarkup:
        confirm_leave_the_team = InlineKeyboardMarkup(row_width=2)

        ib_yes_confirm_leave_the_team = InlineKeyboardButton('Да',
                                                             callback_data=f'confirm_leave_the_team')
        ib_no_confirm_leave_the_team = InlineKeyboardButton('Нет', callback_data=f'back_to_team')

        confirm_leave_the_team.add(ib_yes_confirm_leave_the_team).insert(ib_no_confirm_leave_the_team)
        return confirm_leave_the_team

    @staticmethod
    async def get_confirm_disband_team(team_id: int) -> InlineKeyboardMarkup:
        confirm_disband_team = InlineKeyboardMarkup(row_width=2)

        ib_yes_confirm_disband_team = InlineKeyboardButton('Да',
                                                           callback_data=f'confirm_disband_team?team_id={team_id}')
        ib_no_confirm_disband_team = InlineKeyboardButton('Нет', callback_data=f'back_to_team')

        confirm_disband_team.insert(ib_yes_confirm_disband_team).insert(ib_no_confirm_disband_team)

        return confirm_disband_team

    async def get_generate_invite_code_ikb(self, team_id: int) -> InlineKeyboardMarkup:
        generate_invite_code_ikb = InlineKeyboardMarkup(row_width=1)

        generate_invite_code_ikb.add(
            InlineKeyboardButton('Сгенерировать новый код', callback_data=f'generate_invite_code?team_id={team_id}'))

        generate_invite_code_ikb.add(self.ib_back_to_team)

        return generate_invite_code_ikb

    async def get_team_composition_ikb(self, players: list, captain, is_captain: bool, verification_team: bool) -> InlineKeyboardMarkup:
        team_composition_ikb = InlineKeyboardMarkup(row_width=1)
        captain_ib = InlineKeyboardButton(f'⚜ {captain.username}', url=f'https://t.me/{captain.username}')
        team_composition_ikb.add(captain_ib)

        count_players = len(players) - 1

        for player in players:
            if player is not None:
                team_composition_ikb.add(InlineKeyboardButton(player.username, url=f'https://t.me/{player.username}'))
                if is_captain and not verification_team:
                    team_composition_ikb.add(
                        InlineKeyboardButton('Кикнуть', callback_data=f'kick_team_player?player_id={player.id}'))

        for i in range(4 - count_players):
            team_composition_ikb.add(InlineKeyboardButton('Пусто', callback_data=' '))

        team_composition_ikb.add(self.ib_back_to_team)
        return team_composition_ikb
