from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team_player.status import TeamPlayerStatus
from tg_bot.types.request.status import RequestStatus


async def check_team_player(call, team_player, db_model, team_player_kb, player_kb, is_participate):
    team_ikb = await player_kb.get_team_ikb()

    if team_player.team_player_status == TeamPlayerStatus.ACTIVE:
        team_id = team_player.team_id
        team = await db_model.get_team_by_id(team_id=team_id)

        team_ikb = await team_player_kb.get_team_player_ikb(is_captain=team_player.is_captain, team_id=team.id, is_participate=is_participate)

        await call.bot.send_photo(chat_id=call.message.chat.id,
                                  photo=team.photo_telegram_id,
                                  caption='<b>💠 Комадна</b>\n\n'
                                          f'<b>Имя команды</b>: <code>{team.name}</code>\n',
                                  reply_markup=team_ikb)
    elif team_player.team_player_status == TeamPlayerStatus.KICK:
        await call.message.answer('Вы были кикнуты из команды!', reply_markup=team_ikb)
    elif team_player.team_player_status == TeamPlayerStatus.DISBANDED:
        await call.message.answer('Ваша команда была расформирована!', reply_markup=team_ikb)
    elif team_player.team_player_status == TeamPlayerStatus.LEAVE:
        await call.message.answer('И вот Вы снова один\n'
                                  'Что будете делать?', reply_markup=team_ikb)


async def check_request_team(call, team_player, db_model, team_player_kb, is_participate):
    request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

    if request_team:
        if request_team.request_status == RequestStatus.WAIT:
            await call.message.answer('Ваша заявка на участие в турнире ожидает рассмотрения.')
            return True
        elif request_team.request_status == RequestStatus.PROCESS:
            await call.message.answer('Ваша заявка на участие в турнире на рассмотрении.')
            return True
        elif request_team.request_status == RequestStatus.FAIL:
            message_text = '<b>Вы не прошли верификацию команды.</b>\n\n' \
                           'По причине:\n' \
                           f'{request_team.comment}'
            set_team_ikb = await team_player_kb.get_set_team_ikb(team_id=request_team.team_id)
            await call.message.answer(message_text, reply_markup=set_team_ikb)
            return True
        elif request_team.request_status == RequestStatus.SUCCESS:
            team = await db_model.get_team_by_id(team_id=request_team.team_id)

            team_ikb = await team_player_kb.get_team_player_ikb(is_captain=team_player.is_captain, team_id=team.id, is_tool_park=True, is_participate=is_participate)

            await call.bot.send_photo(chat_id=call.message.chat.id,
                                      photo=team.photo,
                                      caption='<b>💠 Комадна</b>\n\n'
                                              f'<b>Имя команды</b>: <code>{team.name}</code>\n',
                                      reply_markup=team_ikb)
            return True

    return False


async def menu_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    bot = call.bot
    db_model = bot.get('db_model')
    team_player = await db_model.get_team_player(user_id=call.from_user.id)
    team_player_kb = bot.get('kb').get('team_player')
    player_kb = bot.get('kb').get('player')

    response = await check_request_team(call=call, team_player=team_player, db_model=db_model, team_player_kb=team_player_kb, is_participate=team_player.is_participate)

    if not response:
        await check_team_player(call=call, team_player=team_player, db_model=db_model, team_player_kb=team_player_kb, player_kb=player_kb, is_participate=team_player.is_participate)


def register_handlers_menu_team(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team, text=['team', 'back_to_team'], state='*', is_team_player=True)
