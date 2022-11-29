from aiogram import Dispatcher, types
from tg_bot.types.request.status import RequestStatus
from aiogram.dispatcher import FSMContext


async def team_composition(call: types.CallbackQuery, state: FSMContext):
    await call.answer(' ')
    await state.finish()

    user_id = call.from_user.id

    db_model = call.bot.get('db_model')
    team_player_kb = call.bot.get('kb').get('team_player')

    team_player = await db_model.get_team_player(user_id=user_id)

    team_id = team_player.team_id

    team_players = await db_model.get_team_players(team_id=team_id)

    team_player_captain = await db_model.get_captain_by_team_id(team_id=team_id)
    captain = await db_model.get_player_by_id(team_player_captain.player_id)

    request_team = await db_model.get_request_team_by_team_id(team_id=team_id)

    verification_team = False

    if request_team:
        if request_team.request_team_status == RequestStatus.WAIT or request_team.request_team_status == RequestStatus.PROCESS:
            verification_team = True

    players = []

    for team_player in team_players:
        if not team_player.is_captain:
            player = await db_model.get_player_by_id(player_id=team_player.player_id)
            players.append({
                'id': player.id,
                'username': player.username,
                'tg_username': player.tg_username,
                'is_participate': team_player.is_participate
            })

    team_composition_ikb = await team_player_kb.get_team_composition_ikb(players=players,
                                                                         captain=captain,
                                                                         is_captain=team_player.is_captain,
                                                                         verification_team=verification_team)

    await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                             reply_markup=team_composition_ikb)


def register_handlers_team_composition(dp: Dispatcher):
    dp.register_callback_query_handler(team_composition, text=['team_composition'], is_team_player=True, state='*')
