import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_

from tg_bot.models.db_model.models import UserTG, Team, RequestMember, Member, Moderator, Player, TeamPlayer, \
    TeamStatus, Institution, RequestTeam, TournamentTeam, Registration, Match
from tg_bot.models.db_model.db_client import DBClient

from tg_bot.types.moderator.rule import ModeratorRule
from tg_bot.types.team_player.status import TeamPlayerStatus
from tg_bot.types.game.format import FormatGame
from tg_bot.types.match.status import MatchStatus


class DBInteraction(DBClient):
    def __init__(self, sqlalchemy_url: str, base):
        super().__init__(sqlalchemy_url, base)
        self.connect = sessionmaker(bind=self.engine)
        self.session = self.connect()

    async def get_users(self):
        users = self.session.query(UserTG).all()

        return users

    async def add_institution(self, name: str, institution_type: str) -> None:
        self.session.add(Institution(
            name=name,
            institution_type=institution_type
        ))
        self.session.commit()

    async def get_institutions(self, institution_type):
        institutions = self.session.query(Institution).filter(Institution.institution_type == institution_type).all()

        return institutions

    async def get_institution(self, institution_id: int, institution_type: str) -> Institution:
        institution = self.session.query(Institution).filter(
            and_(Institution.id == institution_id, Institution.institution_type == institution_type)).first()

        return institution

    async def user_exist(self, user_id: int) -> bool:
        users = self.session.query(UserTG).filter(UserTG.id == user_id).all()
        user_exist = bool(len(users))
        return user_exist

    async def add_user(self, user_id: int, username):
        user = UserTG(
            id=user_id,
            username=username
        )
        self.session.add(user)
        self.session.commit()

        return user

    async def get_users(self):
        users = self.session(UserTG).all()

        return users

    async def moderator_exist(self, user_id: int) -> bool:
        moderator = self.session.query(Moderator).filter(Moderator.user_id == user_id).all()

        return bool(len(moderator))

    async def add_moderator(self, user_id: int, rule: str):
        moderator = Moderator(
            user_id=user_id,
            rule=rule
        )
        self.session.add(moderator)
        self.session.commit()

    async def get_moderators(self, rule: str):
        moderators = self.session.query(Moderator).filter(
            or_(Moderator.moderator_rule == rule, Moderator.moderator_rule == ModeratorRule.ALL)).all()

        return moderators

    async def request_member_exist(self, user_id: int) -> bool:
        requests_member = self.session.query(RequestMember).filter(RequestMember.user_id == user_id).all()
        request_member_exist = bool(len(requests_member))

        return request_member_exist

    async def add_request_member(self, user_id: int, last_name: str, first_name: str, patronymic: str,
                                 document_photo: str, group: str, institution: str,
                                 member_type: str):
        request_member = RequestMember(
            user_id=user_id,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            document_photo=document_photo,
            group=group,
            institution=institution,
            member_type=member_type
        )

        self.session.add(request_member)
        self.session.commit()

    async def set_request_member_comment(self, user_id: int, comment: str):
        self.session.query(RequestMember).filter(RequestMember.user_id == user_id).update({'comment': comment})
        self.session.commit()

    async def set_request_member_status(self, user_id: int, status: str):
        self.session.query(RequestMember).filter(RequestMember.user_id == user_id).update(
            {'request_member_status': status})
        self.session.commit()

    async def get_request_member(self, user_id: int):
        request_member = self.session.query(RequestMember).filter(RequestMember.user_id == user_id).order_by(
            RequestMember.id.desc()).first()

        return request_member

    async def member_exist(self, user_id: int) -> bool:
        members = self.session.query(Member).filter(Member.user_id == user_id).all()
        member_exist = bool(len(members))

        return member_exist

    async def add_member(self, user_id: int, last_name: str, first_name: str, patronymic: str,
                         institution: str, member_type: str, group: str):
        member = Member(
            user_id=user_id,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            institution=institution,
            group=group,
            member_type=member_type,
        )
        self.session.add(member)
        self.session.commit()

    async def get_member(self, user_id: int) -> Member:
        member = self.session.query(Member).filter(Member.user_id == user_id).first()

        return member

    async def get_member_by_id(self, member_id: int):
        member = self.session.query(Member).filter(Member.id == member_id).first()

        return member

    async def get_members_by_players(self, players: list):
        members = list()

        for player in players:
            member = self.session.query(Member).filter(Member.player_id == player.id).first()
            members.append(member)

        return members

    async def player_exist(self, user_id: int) -> bool:
        if not await self.member_exist(user_id=user_id):
            return False

        member = await self.get_member(user_id=user_id)

        players = self.session.query(Player).filter(Player.member_id == member.id).all()
        player_exist = bool(len(players))

        return player_exist

    async def add_player(self, user_id: int, username: str, discord: str, fastcup: str):
        member = await self.get_member(user_id=user_id)

        player = Player(
            member_id=member.id,
            username=username,
            discord=discord,
            fastcup=fastcup
        )
        self.session.add(player)
        self.session.commit()
        self.session.commit()

    async def get_player_by_id(self, player_id: int) -> Player:
        player = self.session.query(Player).filter(Player.id == player_id).first()

        return player

    async def get_player(self, user_id: int):
        member = await self.get_member(user_id=user_id)

        if member is None:
            return False

        player = self.session.query(Player).filter(Player.member_id == member.id).first()

        return player

    async def set_player_username(self, user_id: int, username: str):
        member = await self.get_member(user_id=user_id)

        self.session.query(Player).filter(Player.member_id == member.id).update({'username': username})

        self.session.commit()

    async def set_player_fastcup(self, user_id: int, fastcup: str):
        member = await self.get_member(user_id=user_id)

        self.session.query(Player).filter(Player.member_id == member.id).update({'fastcup': fastcup})

        self.session.commit()

    async def set_player_discord(self, user_id: int, discord: str):
        member = await self.get_member(user_id=user_id)

        self.session.query(Player).filter(Player.member_id == member.id).update({'username': discord})

        self.session.commit()


    async def get_players(self, team_players, captain_id: int):
        players = list()

        for team_player in team_players:
            player = self.session.query(Player).filter(
                and_(Player.id == team_player.player_id, Player.id != captain_id)).first()
            players.append(player)

        return players

    async def validation_player_username(self, username: str) -> bool:
        players = self.session.query(Player).filter(Player.username == username).all()

        is_valid_username = bool(len(players))

        return is_valid_username

    async def validation_player_discord(self, discord: str) -> bool:
        players = self.session.query(Player).filter(Player.discord == discord).all()

        is_valid_discord = bool(len(players))

        return is_valid_discord

    async def validation_player_fastcup(self, fastcup: str) -> bool:
        players = self.session.query(Player).filter(Player.fastcup == fastcup).all()

        is_valid_fastcup = bool(len(players))

        return is_valid_fastcup

    async def is_team_player(self, user_id: int) -> bool:
        player = await self.get_player(user_id=user_id)

        team_player = self.session.query(TeamPlayer).filter(TeamPlayer.player_id == player.id).all()

        is_team_player = bool(len(team_player))

        return is_team_player

    async def team_player_exist(self, user_id: int):
        player = await self.get_player(user_id=user_id)

        team_players = self.session.query(TeamPlayer).filter(TeamPlayer.player_id == player.id).all()

        team_player_exist = bool(len(team_players))

        return team_player_exist

    async def add_team_player(self, user_id: int, team_id: int, is_captain: bool = False, is_participate: bool = True):
        player = await self.get_player(user_id=user_id)

        team_player = TeamPlayer(
            player_id=player.id,
            team_id=team_id,
            is_participate=is_participate,
            is_captain=is_captain
        )

        self.session.add(team_player)
        self.session.commit()

    async def get_team_player(self, user_id: int) -> TeamPlayer:
        player = await self.get_player(user_id=user_id)

        team_player = self.session.query(TeamPlayer).filter(TeamPlayer.player_id == player.id).order_by(
            TeamPlayer.id.desc()).first()

        return team_player

    async def get_team_player_by_player_id(self, player_id: int) -> TeamPlayer:
        team_player = self.session.query(TeamPlayer).filter(TeamPlayer.player_id == player_id).order_by(
            TeamPlayer.id.desc()).first()

        return team_player

    async def set_team_player_status_by_player_id(self, team_player_id: int, status: str) -> None:
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).update({'team_player_status': status})
        self.session.commit()

    async def set_team_player_status(self, team_player_id: int, status: str) -> None:
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).update({'team_player_status': status})
        self.session.commit()

    async def set_team_player_participate(self, team_player_id: int, is_participate: bool):
        self.session.query(TeamPlayer).filter(TeamPlayer.id == team_player_id).update(
            {'is_participate': is_participate})
        self.session.commit()

    async def get_team_players(self, team_id: int):
        players = self.session.query(TeamPlayer).filter(
            and_(TeamPlayer.team_id == team_id, TeamPlayer.team_player_status == TeamPlayerStatus.ACTIVE)).all()

        return players

    async def get_team_players_without_captain(self, team_id: int, captain_id: int):
        players = self.session.query(TeamPlayer).filter(
            and_(TeamPlayer.team_id == team_id, TeamPlayer.team_player_status == TeamPlayerStatus.ACTIVE, TeamPlayer.id != captain_id)).all()

        return players

    async def get_captain_by_team_id(self, team_id: int) -> TeamPlayer:
        captain = self.session.query(TeamPlayer).filter(
            and_(TeamPlayer.team_id == team_id, TeamPlayer.is_captain)).first()

        return captain

    async def get_team(self, team_id: int) -> Team:
        team = self.session.query(Team).filter(Team.id == team_id).first()

        return team

    async def get_team_by_name(self, name) -> Team:
        team = self.session.query(Team).filter(Team.name == name).first()

        return team

    async def is_valid_invite_code(self, invite_code: str) -> bool:
        invite_codes = self.session.query(Team).filter(
            and_(Team.invite_code == invite_code, Team.team_status == TeamStatus.ACTIVE)).all()

        is_valid_invite_code = bool(len(invite_codes))

        return is_valid_invite_code

    async def set_invite_code(self, team_id: int, invite_code: str):
        self.session.query(Team).filter(Team.id == team_id).update({'invite_code': invite_code})
        self.session.commit()

    async def get_team_by_invite_code(self, invite_code: str) -> Team:
        team = self.session.query(Team).filter(Team.invite_code == invite_code).first()

        return team

    async def get_invite_code(self, team_id):
        team = self.session.query(Team).filter(Team.id == team_id).first()

        return team.invite_code

    async def add_team(self, name: str, photo: str, invite_code: str) -> Team:
        self.session.add(Team(
            name=name,
            photo=photo,
            invite_code=invite_code
        ))
        self.session.commit()

        team = await self.get_team_by_name(name=name)

        return team

    async def get_teams_active(self):
        teams = self.session.query(Team).filter(Team.team_status == TeamStatus.ACTIVE).all()

        return teams

    async def set_team_name(self, team_id: int, name: str):
        self.session.query(Team).filter(Team.id == team_id).update({'name': name})
        self.session.commit()

    async def set_team_photo(self, team_id: int, photo: str):
        self.session.query(Team).filter(Team.id == team_id).update({'photo': photo})
        self.session.commit()

    async def set_team_status(self, team_id: int, status: str):
        self.session.query(Team).filter(and_(Team.id == team_id, Team.team_status == TeamStatus.ACTIVE)).update(
            {'team_status': status})
        self.session.commit()

    async def get_team_by_id(self, team_id) -> Team:
        team = self.session.query(Team).filter(Team.id == team_id).first()

        return team

    async def is_valid_team_name(self, name: str) -> bool:
        teams = self.session.query(Team).filter(and_(Team.name == name, Team.team_status == TeamStatus.ACTIVE)).all()

        is_valid_team_name = bool(len(teams))
        return is_valid_team_name

    async def add_request_team(self, team_id: int):
        self.session.add(RequestTeam(
            team_id=team_id
        ))
        self.session.commit()

    async def set_request_team_comment(self, request_team_id: int, comment: str):
        self.session.query(RequestTeam).filter(RequestTeam.id == request_team_id).update({'comment': comment})
        self.session.commit()

    async def set_request_team_status(self, request_team_id: int, status: str):
        self.session.query(RequestTeam).filter(RequestTeam.id == request_team_id).update(
            {'request_status': status})
        self.session.commit()

    async def get_request_team(self, request_team_id: int):
        request_team = self.session.query(RequestTeam).filter(RequestTeam.id == request_team_id).order_by(
            RequestTeam.id.desc()
        ).first()

        return request_team

    async def get_request_team_by_team_id(self, team_id: int):
        request_team = self.session.query(RequestTeam).filter(RequestTeam.team_id == team_id).order_by(
            RequestTeam.id.desc()).first()

        return request_team

    async def add_tournament_team(self, captain_id: int, players: list,
                                  name: str, photo: str):
        self.session.add(TournamentTeam(
            captain_id=captain_id,
            second_player=players[0].id,
            third_player=players[1].id,
            four_player=players[2].id,
            fifth_player=players[3].id,
            name=name,
            photo=photo,
        ))
        self.session.commit()

    async def set_tournament_team_group(self, tournament_team_id: int, group: str):
        self.session.query(TournamentTeam).filter(TournamentTeam.id == tournament_team_id).update({'group': group})
        self.session.commit()

    async def get_tournament_team_by_id(self, tournament_team_id: int):
        tournament_team = self.session.query(TournamentTeam).filter(TournamentTeam.id == tournament_team_id).first()

        return tournament_team

    async def get_tournament_teams(self):
        tournament_teams = self.session.query(TournamentTeam).all()

        return tournament_teams

    async def get_tournament_teams_by_group(self, group: str):
        tournament_teams = self.session.query(TournamentTeam).filter(TournamentTeam.group == group).all()

        return tournament_teams

    async def get_all_team_players(self):
        team_players = self.session.query(TeamPlayer).all()

        return team_players

    async def add_registration(self, opening_date: float, limit_teams: int):
        self.session.add(Registration(
            opening_date=opening_date,
            limit_teams=limit_teams
        ))
        self.session.commit()

    async def get_registration(self):
        try:
            registration = self.session.query(Registration).order_by(Registration.id.desc()).first()

            return registration
        except Exception as ex:
            print(ex)

    async def set_registration_status(self, registration_id: int, status: str):
        self.session.query(Registration).filter(Registration.id == registration_id).update({'registration_status': status})
        self.session.commit()

    async def set_data_close_registration(self, registration_id: int, closing_date: float):
        self.session.query(Registration).filter(Registration.id == registration_id).update({'closing_date': closing_date})

    async def and_match(self, first_team_id: int, second_team_id: int, stage: str):
        self.session.add(Match(
            first_team_id=first_team_id,
            second_team_id=second_team_id,
            stage=stage
        ))

        self.session.commit()