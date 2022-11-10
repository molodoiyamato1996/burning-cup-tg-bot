from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team_player.status import TeamPlayerStatus


async def leave_the_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    team_player_kb = call.bot.get('kb').get('team_player')

    confirm_leave_the_team_ikb = await team_player_kb.get_confirm_leave_the_team_ikb()

    await call.message.answer('Вы уверенны, что хотите покинуть команду?', reply_markup=confirm_leave_the_team_ikb)


async def confirm_leave_the_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')

    team_player = await db_model.get_team_player(user_id=user_id)
    await db_model.set_team_player_status(team_player_id=team_player.id, status=TeamPlayerStatus.LEAVE)
    await call.message.answer('Вы успешно покинули команду!')


def register_handlers_leave_the_team(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_leave_the_team, text_contains=['confirm_leave_the_team'], state='*', is_team_player=True)
    dp.register_callback_query_handler(leave_the_team, text_contains=['leave_the_team'], state='*', is_team_player=True)
