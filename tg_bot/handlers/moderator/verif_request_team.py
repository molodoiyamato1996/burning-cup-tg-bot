import datetime
import math

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.registration.status import RegistrationStatus
from tg_bot.types.moderator.states.verif_request_team import VerifRequestTeam
from tg_bot.types.request.status import RequestStatus

from tg_bot.misc.parse import parse_callback
from tg_bot.misc.notify import notify_user
from tg_bot.misc.matches import grouping, add_opening_matches


async def view_request_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await state.finish()

    db_model = call.bot.get('db_model')
    moderator_kb = call.bot.get('kb').get('moderator')

    props = await parse_callback('view_request_team', call.data)

    team_id = props.get('team_id')

    team = await db_model.get_team(team_id=team_id)
    registration = await db_model.get_registration()

    if registration.registration_status == RegistrationStatus.CLOSE:
        await call.message.answer('Регистрация закрыта!')
        return

    request_team = await db_model.get_request_team_by_team_id(team_id=team_id)

    if request_team.request_status != RequestStatus.WAIT:
        await call.message.answer('Анкета уже верифицируется.')
        return

    await db_model.set_request_team_status(request_team_id=request_team.id, status=RequestStatus.PROCESS)
    verif_request_team_ikb = await moderator_kb.get_verif_request_team_ikb(request_team_id=request_team.id)
    message_text = '<b>Верификация команды</b>\n\n' \
                   f'Название команды: <code>{team.name}</code>\n\n' \
                   f'<b>Верифицировать команду?</b>'

    await call.bot.send_photo(
        chat_id=call.message.chat.id,
        photo=team.photo,
        caption=message_text,
        reply_markup=verif_request_team_ikb
    )


async def verif_request_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer()

    db_model = call.bot.get('db_model')

    props = await parse_callback('verif_request_team', call.data)

    request_team_id = props.get('request_team_id')
    result = props.get('result')
    registration = await db_model.get_registration()

    if registration.registration_status == RegistrationStatus.CLOSE:
        await call.message.answer('Регистрация закрыта!')
        return

    if result == 'yes':
        request_team = await db_model.get_request_team(request_team_id=request_team_id)

        captain = await db_model.get_captain_by_team_id(team_id=request_team.team_id)
        team_players = await db_model.get_team_players_without_captain(team_id=request_team.team_id,
                                                                       captain_id=captain.id)
        team = await db_model.get_team(team_id=request_team.id)

        await db_model.add_tournament_team(
            captain_id=captain.id,
            players=team_players,
            name=team.name,
            photo=team.photo,
        )

        tournament_teams = await db_model.get_tournament_teams()

        if len(tournament_teams) == registration.limit_teams:
            await db_model.set_registration_status(registration_id=registration.id, status=RegistrationStatus.CLOSE)

            closing_date = datetime.datetime.now().timestamp()
            await db_model.set_registration_closing_date(registration_id=registration.id, closing_date=closing_date)
            users = await db_model.get_users()

            await grouping(db_model=db_model)
            await add_opening_matches(db_model=db_model)

            for user in users:
                await notify_user(
                    text='Регистрация на турнир закончена <b>🔥 Burning Cup</b>\n\n'
                         'Команды и матчи можете посмотреть на сайте https://www.burning-cup.com',
                    chat_id=user.id,
                    call=call
                )

        await db_model.set_request_team_status(request_team_id=request_team_id, status=RequestStatus.SUCCESS)

        player_captain = await db_model.get_player_by_id(player_id=captain.id)
        member_captain = await db_model.get_member_by_id(member_id=player_captain.member_id)

        await notify_user(
            text='✅ Ваша команда приняла участие в турнире <b>🔥 Burning Cup</b>',
            chat_id=member_captain.user_id,
            call=call
        )
    else:
        await call.message.answer('Введите причину отказа')
        await state.set_state(VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM)
        async with state.proxy() as data:
            data['request_team_id'] = request_team_id


async def enter_comment_request_team(msg: types.Message, state=FSMContext):
    comment = msg.text

    db_model = msg.bot.get('db_model')

    team_player_kb = msg.bot.get('kb').get('team_player')

    state_data = await state.get_data()

    request_team_id = state_data.get('request_team_id')

    await db_model.set_request_team_comment(request_team_id=request_team_id, comment=comment)
    request_team = await db_model.get_request_team(request_team_id=request_team_id)

    team_player_captain = await db_model.get_captain_by_team_id(team_id=request_team.team_id)
    player = await db_model.get_player_by_id(player_id=team_player_captain.player_id)
    member = await db_model.get_member_by_id(member_id=player.member_id)

    set_team_ikb = await team_player_kb.get_set_team_ikb(team_id=request_team.team_id)
    message_text = '<b>Вы не прошли верификацию команды.</b>\n\n' \
                   'По причине:\n' \
                   f'{request_team.comment}'

    await notify_user(
        chat_id=member.user_id,
        text=message_text,
        reply_markup=set_team_ikb,
        msg=msg
    )


def register_handlers_verif_request_team(dp: Dispatcher):
    dp.register_callback_query_handler(view_request_team, text_contains=['view_request_team'], state='*')
    dp.register_callback_query_handler(verif_request_team, text_contains=['verif_request_team'], state='*')
    dp.register_message_handler(enter_comment_request_team, state=VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM)
