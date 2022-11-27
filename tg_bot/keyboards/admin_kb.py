from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.types.registration import RegistrationStatus


class AdminKb:
    def __init__(self):
        self.tournament_teams = InlineKeyboardButton('Турнирые команды', callback_data='tournament_teams')

        self.registration = InlineKeyboardButton('Регистрация', callback_data='registration')
        self.days = InlineKeyboardButton('Дни', callback_data='days')
        self.games = InlineKeyboardButton('Игры', callback_data='games')
        self.matches = InlineKeyboardButton('Матчи', callback_data='matches')
        self.maps = InlineKeyboardButton('Карты', callback_data='maps')

        self.tournaments = InlineKeyboardButton('Турниры', callback_data='tournaments')
        self.players = InlineKeyboardButton('Игроки', callback_data='players')
        self.team_players = InlineKeyboardButton('Командные игроки', callback_data='team_players')
        self.users = InlineKeyboardButton('Пользователи', callback_data='users')
        self.teams = InlineKeyboardButton('Команды', callback_data='teams')

        self.add_match = InlineKeyboardButton('Добавить матч', callback_data='add_match')
        self.get_matches = InlineKeyboardButton('Получить матчи', callback_data='get_matches')
        self.set_match = InlineKeyboardButton('Изменить матч', callback_data='set_match')

        self.open_registration = InlineKeyboardButton('Назначить регистрацию', callback_data='open_registration')
        self.set_registration = InlineKeyboardButton('Изменить регистрацию', callback_data='set_registration')
        self.cancel_registration = InlineKeyboardButton('Отменить регистрацию', callback_data='cancel_registration')
        self.view_registration_conf = InlineKeyboardButton('Посмотреть регистрацию', callback_data='view_registration')

        self.back_to_registration = InlineKeyboardButton('Вернуться', callback_data='back_to_registration')

        self.view_tournament_teams = InlineKeyboardButton('Показать команды', callback_data='view_teams')
        self.block_team = InlineKeyboardButton('Заблокировать команду', callback_data='block_team')

    async def get_menu_tournament_teams_ikb(self, tournament_teams: list) -> InlineKeyboardMarkup:
        menu_tournament_teams_ikb = InlineKeyboardMarkup(row_width=1)

        for tournament_team in tournament_teams:
            menu_tournament_teams_ikb.add(InlineKeyboardButton(
                text=tournament_team.name, callback_data=f'view_tournament_team?tournament_team_id={tournament_team.id}'
            ))

        return menu_tournament_teams_ikb

    async def get_menu_tournament_management_ikb(self, registration) -> InlineKeyboardMarkup:
        menu_tournaments_ikb = InlineKeyboardMarkup(row_width=1)

        menu_tournaments_ikb.add(self.registration)

        if registration:
            if registration.registration_status != RegistrationStatus.WAIT:
                menu_tournaments_ikb.add(self.tournament_teams)

            if registration.registration_status == RegistrationStatus.CLOSE:
                menu_tournaments_ikb.add(self.days).add(self.games).add(self.matches)

        return menu_tournaments_ikb

    async def get_menu_tournaments_ikb(self, is_tournament: bool) -> InlineKeyboardMarkup:
        menu_tournaments_ikb = InlineKeyboardMarkup(row_width=1)

        if is_tournament:
            menu_tournaments_ikb.add(InlineKeyboardButton(
                'Управление', callback_data='tournament_management'
            ))
        else:
            menu_tournaments_ikb.add(InlineKeyboardButton(
                'Назначить турнир', callback_data='add_tournament'
            ))

        return menu_tournaments_ikb

    async def get_add_day_choice_game_ikb(self, game) -> InlineKeyboardMarkup:
        add_day_choice_game_ikb = InlineKeyboardMarkup(row_width=1)

        add_day_choice_game_ikb.add(
            InlineKeyboardButton(f'{game.get("first_tournament_team").photo} vs {game.get("second_tournament_team").photo}', callback_data=f'add_days_choice_game?game_id={game.id}')
        )


        return add_day_choice_game_ikb

    async def get_menu_days_ikb(self) -> InlineKeyboardMarkup:
        menu_days_ikb = InlineKeyboardMarkup(row_width=1)

        add_day = InlineKeyboardButton('Добавить', callback_data='add_day')
        delete_day = InlineKeyboardButton('Удалить', callback_data='delete_day')
        set_day = InlineKeyboardButton('Изменить', callback_data='set_day')

        menu_days_ikb.add(add_day).add(delete_day).add(set_day)

        return menu_days_ikb

    async def get_choice_team_ikb(self, first_team, second_team, game_id: int) -> InlineKeyboardMarkup:
        choice_team_ikb = InlineKeyboardMarkup(row_width=1)

        ib_first_team = InlineKeyboardButton(first_team.name, callback_data=f'choice_team?team_id={first_team.id}&game_id={game_id}')
        ib_second_team = InlineKeyboardButton(second_team.name, callback_data=f'choice_team?team_id={second_team.id}&game_id={game_id}')

        choice_team_ikb.add(ib_first_team).add(ib_second_team)

        return choice_team_ikb

    async def get_choice_game_ikb(self, games: list) -> InlineKeyboardMarkup:
        choice_game_ikb = InlineKeyboardMarkup(row_width=1)

        for game in games:
            choice_game_ikb.add(
                InlineKeyboardButton(f'{game.get("first_match_team").name} vs {game.get("second_match_team").name}',
                                     callback_data=f'choice_game?game_id={game.get("id")}&first_team_id={game.get("first_match_team").id}&second_team_id={game.get("second_match_team").id}')
            )

        return choice_game_ikb

    async def get_add_game_ikb(self, matches: list) -> InlineKeyboardMarkup:
        add_game_ikb = InlineKeyboardMarkup(row_width=1)

        for match in matches:
            add_game_ikb.add(
                InlineKeyboardButton(f'{match.get("first_match_team").name} vs {match.get("second_match_team").name}', callback_data=f'choice_match?match_id={match.get("id")}')
            )

        return add_game_ikb

    async def get_games_ikb(self) -> InlineKeyboardMarkup:
        games_ikb = InlineKeyboardMarkup(row_width=1)

        ibs_games_ikb = [
            InlineKeyboardButton('Добавить игру', callback_data='add_game'),
            InlineKeyboardButton('Обновить результаты игры', callback_data='update_result_game'),
        ]

        games_ikb.add(*ibs_games_ikb)

        return games_ikb

    async def get_match_ikb(self) -> InlineKeyboardMarkup:
        match_ikb = InlineKeyboardMarkup(row_width=1)

        ibs_match_ikb = [
            InlineKeyboardButton('Обновить результаты матча', callback_data='add_game')
        ]

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
            self.tournaments,
            self.teams,
            self.team_players,
            self.users
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

    async def get_registration_ikb(self, registration) -> InlineKeyboardMarkup:
        registration_ikb = InlineKeyboardMarkup(row_width=1)

        registration_buttons = []

        if registration:
            if registration.registration_status != RegistrationStatus.CLOSE:
                registration_buttons.append(self.set_registration)
                registration_buttons.append(self.cancel_registration)
            registration_buttons.append(self.view_registration_conf)
        else:
            registration_buttons.append(self.open_registration)

        registration_ikb.add(*registration_buttons)

        return registration_ikb

    async def get_back_to_registration_ikb(self) -> InlineKeyboardMarkup:
        back_to_registration_ikb = InlineKeyboardMarkup(row_width=1)

        back_to_registration_ikb.add(self.back_to_registration)

        return back_to_registration_ikb

    async def get_view_tournament_teams_ikb(self, tournament_teams: list) -> InlineKeyboardMarkup:
        view_tournament_teams_ikb = InlineKeyboardMarkup(row_width=1)

        for tournament_team in tournament_teams:
            view_tournament_teams_ikb.add(
                InlineKeyboardButton(tournament_team.name, callback_data=f'view_tournament_team?id={tournament_team.id}')
            )

        return view_tournament_teams_ikb
