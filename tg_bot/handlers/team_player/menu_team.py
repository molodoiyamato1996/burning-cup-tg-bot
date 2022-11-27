from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team_player.status import TeamPlayerStatus
from tg_bot.types.request.status import RequestStatus


async def menu_team_block(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id

    db_model = call.bot.get('db_model')
    player_kb = call.bot.get('kb').get('player')
    team_player_kb = call.bot.get('kb').get('team_player')

    team_player = await db_model.get_team_player(user_id=user_id)

    request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

    if request_team:
        if request_team.request_status == RequestStatus.WAIT:
            await call.message.answer('Ваша заявка на участие в турнире ожидает рассмотрения.')
            return
        elif request_team.request_status == RequestStatus.PROCESS:
            await call.message.answer('Ваша заявка на участие в турнире на рассмотрении.')
            return
        elif request_team.request_status == RequestStatus.FAIL:
            message_text = '<b>Вы не прошли верификацию команды.</b>\n\n' \
                           'По причине:\n' \
                           f'{request_team.comment}'
            set_team_ikb = await team_player_kb.get_set_team_ikb(team_id=request_team.team_id)
            await call.message.answer(message_text, reply_markup=set_team_ikb)
            return
        elif request_team.request_status == RequestStatus.SUCCESS:
            team = await db_model.get_team_by_id(team_id=request_team.team_id)

            team_ikb = await player_kb.get_team_player_ikb(is_captain=team_player.is_captain, team_id=team.id, is_tool_park=True)

            await call.bot.send_photo(chat_id=call.message.chat.id,
                                      photo=team.photo,
                                      caption='<b>💠 Комадна</b>\n\n'
                                              f'<b>Имя команды</b>: <code>{team.name}</code>\n',
                                      reply_markup=team_ikb)
            return


async def menu_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    user_id = call.from_user.id

    db_model = call.bot.get('db_model')
    player_kb = call.bot.get('kb').get('player')
    team_player_kb = call.bot.get('kb').get('team_player')

    team_player = await db_model.get_team_player(user_id=user_id)

    if team_player.team_player_status == TeamPlayerStatus.ACTIVE:
        team_id = team_player.team_id
        team = await db_model.get_team_by_id(team_id=team_id)

        team_ikb = await player_kb.get_team_player_ikb(is_captain=team_player.is_captain, team_id=team.id)

        await call.bot.send_photo(chat_id=call.message.chat.id,
                                  photo=team.photo_telegram_id,
                                  caption='<b>💠 Комадна</b>\n\n'
                                          f'<b>Имя команды</b>: <code>{team.name}</code>\n',
                                  reply_markup=team_ikb)

    team_ikb = await player_kb.get_team_ikb()

    if team_player.team_player_status == TeamPlayerStatus.KICK:
        await call.message.answer('Вы были кикнуты из команды!', reply_markup=team_ikb)
    elif team_player.team_player_status == TeamPlayerStatus.DISBANDED:
        await call.message.answer('Ваша команда была расформирована!', reply_markup=team_ikb)
    elif team_player.team_player_status == TeamPlayerStatus.LEAVE:
        await call.message.answer('И вот Вы снова один\n'
                                  'Что будете делать?', reply_markup=team_ikb)


async def back_to_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    user_id = call.from_user.id

    db_model = call.bot.get('db_model')
    player_kb = call.bot.get('kb').get('player')

    team_player = await db_model.get_team_player(user_id=user_id)

    request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

    if team_player.team_player_status == TeamPlayerStatus.ACTIVE:
        team_id = team_player.team_id

        team = await db_model.get_team_by_id(team_id=team_id)
        is_tool_park = True if request_team.request_status == RequestStatus.SUCCESS else False
        team_ikb = await player_kb.get_team_player_ikb(is_captain=team_player.is_captain, team_id=team.id, is_tool_park=is_tool_park)

        await call.bot.edit_message_caption(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            caption='<b>💠 Комадна</b>\n\n'
                                                    f'<b>Имя команды</b>: <code>{team.name}</code>\n',
                                            reply_markup=team_ikb)

    team_ikb = await player_kb.get_team_ikb()

    if team_player.team_player_status == TeamPlayerStatus.KICK:
        await call.message.answer('Вы были кикнуты из команды!', reply_markup=team_ikb)
    elif team_player.team_player_status == TeamPlayerStatus.DISBANDED:
        await call.message.answer('Ваша команда была расформирована!', reply_markup=team_ikb)
    elif team_player.team_player_status == TeamPlayerStatus.LEAVE:
        await call.message.answer('И вот Вы снова один\n'
                                  'Что будете делать?', reply_markup=team_ikb)


def register_handlers_menu_team(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team_block, text=['team'], state='*', is_team_player=True)
    dp.register_callback_query_handler(menu_team, text=['team'], state='*', is_team_player=True)
    dp.register_callback_query_handler(back_to_team, text=['back_to_team'], state='*', is_team_player=True)
