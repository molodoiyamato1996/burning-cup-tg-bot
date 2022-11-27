from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.parse import parse_callback
from tg_bot.types.team_player import TeamPlayerStatus
from tg_bot.types.request import RequestStatus
from tg_bot.misc.phares import Phrases


async def kick_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    team_player_kb = call.bot.get('kb').get('team_player')
    db_model = call.bot.get('db_model')

    current_team_player = await db_model.get_team_player(user_id=call.from_user.id)

    request_team = await db_model.get_request_team_by_team_id(team_id=current_team_player.team_id)

    if request_team:
        if request_team.request_team_status == RequestStatus.WAIT or request_team.request_team_status == RequestStatus.PROCESS:
            answer_text = Phrases.captain_verification_block
            await call.message.answer(answer_text)
            return

    props = await parse_callback('kick_team_player', callback_data=call.data)
    player_id = props.get('player_id')

    confirm_kick_team_player_ikb = await team_player_kb.get_confirm_kick_team_player_ikb(player_id=player_id)
    player = await db_model.get_player_by_id(player_id=player_id)

    answer_text = Phrases.confirm_kick_team_player + f'{player.username}?'

    await call.message.answer(answer_text, reply_markup=confirm_kick_team_player_ikb)


async def confirm_kick_player(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')

    db_model = call.bot.get('db_model')
    props = await parse_callback('confirm_kick_team_player', callback_data=call.data)
    player_id = props.get('player_id')

    team_player = await db_model.get_team_player_by_player_id(player_id=player_id)

    await db_model.set_team_player_status_by_player_id(team_player_id=team_player.id, status=TeamPlayerStatus.KICK)

    answer_text = Phrases.success_kick_team_player

    await call.message.answer(answer_text)


def register_handlers_kick_player(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_kick_player, text_contains=['confirm_kick_team_player'], state='*', is_team_player=True, is_captain=True)
    dp.register_callback_query_handler(kick_player, text_contains=['kick_team_player'], state='*', is_team_player=True, is_captain=True)
