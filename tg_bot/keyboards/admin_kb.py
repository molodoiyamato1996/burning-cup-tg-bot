from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AdminKb:
    def __init__(self):
        self.tournament_teams = InlineKeyboardButton('Турнирые команды', callback_data='tournament_teams')
        self.teams = InlineKeyboardButton('Команды', callback_data='teams')
        self.players = InlineKeyboardButton('Игроки', callback_data='players')
        self.registration = InlineKeyboardButton('Регистрация', callback_data='registration')
        self.tournament_days = InlineKeyboardButton('Турнирые дни', callback_data='tournament_days')
        self.matches = InlineKeyboardButton('Матчи', callback_data='matches')
        self.games = InlineKeyboardButton('Игры', callback_data='games')
        self.maps = InlineKeyboardButton('Карты', callback_data='maps')

        self.add_match = InlineKeyboardButton('Добавить матч', callback_data='add_match')
        self.get_matches = InlineKeyboardButton('Получить матчи', callback_data='get_matches')
        self.set_match = InlineKeyboardButton('Изменить матч', callback_data='set_match')

        self.start_registration = InlineKeyboardButton('Назначить регистрацию', callback_data='start_registration')
        self.set_registration = InlineKeyboardButton('Изменить регистрацию', callback_data='set_registration')
        self.cancel_registration = InlineKeyboardButton('Отменить регистрацию', callback_data='cancel_registration')
        self.view_registration_conf = InlineKeyboardButton('Посмотреть регистрацию', callback_data='view_registration')

        self.back_to_registration = InlineKeyboardButton('Вернуться', callback_data='back_to_registration')

        self.view_tournament_teams = InlineKeyboardButton('Показать команды', callback_data='view_teams')
        self.block_team = InlineKeyboardButton('Заблокировать команду', callback_data='block_team')

    async def get_view_tournament_team_ikb(self, tournament_teams: list) -> InlineKeyboardMarkup:
        view_team_ikb = InlineKeyboardMarkup(row_width=1)

        for tournament_team in tournament_teams:
            view_team_ikb.add(InlineKeyboardButton(
                text=tournament_team.name, callback_data=f'view_tournament_team?tournament_team_id={tournament_team.id}'
            ))

        return view_team_ikb

    async def get_team_ikb(self) -> InlineKeyboardMarkup:
        team_ikb = InlineKeyboardMarkup(row_width=1)

        team_buttons = [
            self.view_tournament_teams,
            self.block_team
        ]

        team_ikb.add(*team_buttons)

        return team_ikb

    async def get_start_ikb(self) -> InlineKeyboardMarkup:
        start_ikb = InlineKeyboardMarkup(row_width=1)

        start_buttons = [
            self.tournament_teams,
            self.teams,
            self.players,
            self.registration,
            self.tournament_days,
            self.matches,
            self.games,
            self.maps,
        ]
        start_ikb.add(*start_buttons)

        return start_ikb

    async def get_matches_ikb(self) -> InlineKeyboardMarkup:
        matches_ikb = InlineKeyboardMarkup(row_width=1)

        matches_buttons = [
            self.add_match,
            self.set_match,
            self.get_matches
        ]

        matches_ikb.add(*matches_buttons)

        return matches_ikb

    async def get_registration_ikb(self, is_registration: bool) -> InlineKeyboardMarkup:
        registration_ikb = InlineKeyboardMarkup(row_width=1)

        registration_buttons = []

        if is_registration:
            registration_buttons.append(self.set_registration)
            registration_buttons.append(self.cancel_registration)
            registration_buttons.append(self.view_registration_conf)
        else:
            registration_buttons.append(self.start_registration)

        registration_ikb.add(*registration_buttons)

        return registration_ikb

    async def get_back_to_registration_ikb(self) -> InlineKeyboardMarkup:
        back_to_registration_ikb = InlineKeyboardMarkup(row_width=1)

        back_to_registration_ikb.add(self.back_to_registration)

        return back_to_registration_ikb

    async def get_match_ikb(self):
        match = InlineKeyboardMarkup(row_width=1)

    async def get_view_tournament_teams_ikb(self, tournament_teams: list) -> InlineKeyboardMarkup:
        view_tournament_teams_ikb = InlineKeyboardMarkup(row_width=1)

        for tournament_team in tournament_teams:
            view_tournament_teams_ikb.add(
                InlineKeyboardButton(tournament_team.name, callback_data=f'view_tournament_team?id={tournament_team.id}')
            )

        return view_tournament_teams_ikb
