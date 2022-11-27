from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def participate(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    team_player_kb = call.bot.get('kb').get('team_player')

    participate_ikb = await team_player_kb.get_confirm_participate_ikb()

    await call.bot.edit_message_caption(caption='<b>🔥 Burning Cup</b>\n\n'
                                                'После того, как Вы и Выша команда подтвердят участие в турнире,\n'
                                                'состав команды уже нельзя будет изменить.\n\n'
                                                'Подтвердить участие?',
                                        chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=participate_ikb)


async def confirm_participate(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')

    team_player = await db_model.get_team_player(user_id=user_id)
    await db_model.set_team_player_participate(team_player_id=team_player.id, is_participate=True)


def register_handlers_participate(dp: Dispatcher):
    dp.register_callback_query_handler(participate, text=['participate'], is_team_player=True)
    dp.register_callback_query_handler(participate, text=['confirm_participate'], is_team_player=True)
