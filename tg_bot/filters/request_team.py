from aiogram.dispatcher.filters import BoundFilter


class RequestTeamFilter(BoundFilter):
    key = 'is_request_team'

    def __init__(self, is_request_team=None):
        self.is_request_team = is_request_team

    async def check(self, obj):
        if self.is_request_team is None:
            return False

        user_id = obj.from_user.id
        db_model = obj.bot.get('db_model')

        team_player = await db_model.team_player(user_id=user_id)
        request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

        return self.is_request_team == request_team_exist