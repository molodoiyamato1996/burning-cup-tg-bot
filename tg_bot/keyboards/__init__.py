from .user_kb import UserKb
from .admin_kb import AdminKb
from .player_kb import PlayerKb
from .team_player_kb import TeamPLayerKb
from .moderator_kb import ModeratorKb
from .member_kb import MemberKb


kb = {
    'user': UserKb(),
    'player': PlayerKb(),
    'team_player': TeamPLayerKb(),
    'moderator': ModeratorKb(),
    'admin': AdminKb(),
    'member': MemberKb(),
}
