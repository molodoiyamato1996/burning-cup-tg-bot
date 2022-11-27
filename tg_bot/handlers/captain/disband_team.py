from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team import TeamStatus
from tg_bot.types.team_player import TeamPlayerStatus

from tg_bot.misc.parse import parse_callback


async def disband_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    team_player_kb = call.bot.get('kb').get('team_player')

    props = await parse_callback('disband_team', call.data)

    team_id = props.get('team_id')

    confirm_disband_team_ikb = await team_player_kb.get_confirm_disband_team(team_id=team_id)
    await call.bot.edit_message_caption(caption='Вы уверенны, что хотите расформировать команду?',
                                        message_id=call.message.message_id,
                                        chat_id=call.message.chat.id,
                                        reply_markup=confirm_disband_team_ikb)


async def confirm_disband_team(call: types.CallbackQuery):
    await call.answer(' ')
    await call.message.delete()

    db_model = call.bot.get('db_model')
    props = await parse_callback('confirm_disband_team', call.data)

    team_id = props.get('team_id')

    team_players = await db_model.get_team_players(team_id=team_id)

    for team_player in team_players:
        await db_model.set_team_player_status(team_player_id=team_player.id, status=TeamPlayerStatus.DISBANDED)

    await db_model.set_team_status(team_id=team_id, status=TeamStatus.DISBANDED)

    await call.message.answer(text='Команда успешно распущена!', reply_markup=None)


def register_handlers_dispand_team(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_disband_team, text_contains=['confirm_disband_team'],
                                       is_team_player=True, is_captain=True)
    dp.register_callback_query_handler(disband_team, text_contains=['disband_team'], state='*', is_team_player=True,
                                       is_captain=True)
