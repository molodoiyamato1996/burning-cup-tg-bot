import os
import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.scripts import parse_callback, notify_user
from tg_bot.misc.matches import grouping, add_matches
from tg_bot.types.moderator import VerifRequestTeam
from tg_bot.types.registration import RegistrationStatus

from tg_bot.types.request import RequestStatus


# view -> moderation -> response
async def menu_team_requests(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    admin_kb = bot.get("kb").get("admin")

    requests_ikb = await admin_kb.get_requests_ikb()

    answer_text = "<b>Запросы</b>\n\n" + "Выбрать действие:"

    await call.message.answer(answer_text, reply_markup=requests_ikb)


async def menu_view_all_team_requests(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    admin_kb = bot.get("kb").get("admin")
    db_model = bot.get("db_model")

    team_requests = await db_model.get_team_requests()
    view_all_requests_ikb = await admin_kb.get_view_all_team_requests_ikb(team_requests=team_requests)

    answer_text = "<b>Запросы</b>\n\n" + "Выберите запрос:"

    await call.message.answer(text=answer_text, reply_markup=view_all_requests_ikb)


async def menu_view_team_request(call: types.CallbackQuery, state: FSMContext):
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    admin_kb = bot.get("kb").get("admin")
    db_model = bot.get("db_model")

    props = await parse_callback("view_team_request", call.data)

    team_request_id = props.get("team_request_id")

    team_request = await db_model.get_team_request(team_request_id=team_request_id)
    team = await db_model.get_team(team_id=team_request.team_id)

    team_player_captain = await db_model.get_captain_by_team_id(team_id=team.id)
    player_captain = await db_model.get_player(player_id=team_player_captain.player_id)

    team_players = await db_model.get_team_players_without_captain(team_id=team.id)

    captain_text = f"<code>{player_captain.username}</code> <code>{player_captain.discord}</code>\n"

    players_text = ""

    for team_player in team_players:
        player = await db_model.get_player(player_id=team_player.player_id)
        players_text += f"<code>{player.username}</code> <code>{player.discord}</code>\n"

    caption = "<b>Запрос команды</b>\n\n" \
              f"Статус: {team_request.request_status}\n" \
              f"Дата подачи: {team_request.date_request}\n" \
              f"Название команды: <code>{team.name}\n\n</code>" \
              f"Состав команды:\n\n" + captain_text + players_text + \
              f"Для отправки:\n" \
              f"<code>Название команды: {team.name}\n\n{captain_text + players_text}</code>"

    moderation_team_request_ikb = await admin_kb.get_moderation_team_request_ikb(team_request_id=team_request.id)

    await bot.send_photo(
        chat_id=call.from_user.id,
        caption=caption,
        photo=team.photo_telegram_id,
        reply_markup=moderation_team_request_ikb
    )


async def moderation_team_request(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer(" ")
    await state.finish()

    bot = call.bot
    props = await parse_callback("moderation_team_request", call.data)
    db_model = bot.get("db_model")
    result = props.get("result")
    team_request_id = props.get("team_request_id")


    tournament = await db_model.get_tournament()
    registration = await db_model.get_registration(tournament_id=tournament.id)

    if registration.registration_status == RegistrationStatus.CLOSE:
        await call.message.answer('Регистрация закрыта!')
        return

    if result == "SUCCESS":
        if registration.registration_status == RegistrationStatus.OPEN:
            request_team = await db_model.get_request_team(request_team_id=team_request_id)

            captain = await db_model.get_captain_by_team_id(team_id=request_team.team_id)
            team_players = await db_model.get_team_players_without_captain(team_id=request_team.team_id,
                                                                           captain_id=captain.id)

            team = await db_model.get_team(team_id=request_team.team_id)

            photo_name = team.name + ".png"
            photo_telegram_id = team.photo_telegram_id
            file = await call.bot.get_file(photo_telegram_id)
            file_path = file.file_path

            directory = call.bot.get("config").get("path").get("images")
            path = os.path.join(directory, photo_name)

            await call.bot.download_file(file_path=file_path, destination_dir=path)

            await db_model.set_team_photo(team_id=team.id, photo=photo_name)

            await db_model.add_tournament_team(
                captain_id=captain.id,
                players=team_players,
                name=team.name,
                photo=photo_name,
            )

            tournament_teams = await db_model.get_tournament_teams()

            if len(tournament_teams) == tournament.limit_teams:
                await db_model.set_registration_status(registration_id=registration.id, status=RegistrationStatus.CLOSE)

                closing_date = datetime.datetime.now()
                await db_model.set_registration_closing_date(registration_id=registration.id, closing_date=closing_date)
                users = await db_model.get_users()

                await db_model.set_request_team_status(request_team_id=team_request_id, status=RequestStatus.SUCCESS)

                player_captain = await db_model.get_player(player_id=captain.player_id)
                member_captain = await db_model.get_member(member_id=player_captain.member_id)

                await notify_user(
                    text='✅ Ваша команда приняла участие в турнире <b>🔥 Burning Cup</b>',
                    chat_id=member_captain.user_id,
                    bot=call.bot
                )

                await grouping(db_model=db_model)
                await add_matches(db_model=db_model)

                for user in users:
                    await notify_user(
                        text='Регистрация на турнир закончена <b>🔥 Burning Cup</b>\n\n'
                             'Команды и матчи можете посмотреть на сайте https://www.burning-cup.com',
                        chat_id=user.id,
                        bot=call.bot
                    )
    elif result == "FAIL":
        await call.message.answer('Введите причину отказа')
        await state.set_state(VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM)
        async with state.proxy() as data:
            data['request_team_id'] = team_request_id


async def enter_comment_team_request(msg: types.Message, state: FSMContext):
    await msg.delete()

    comment = msg.text

    db_model = msg.bot.get('db_model')

    state_data = await state.get_data()

    request_team_id = state_data.get('request_team_id')

    await db_model.set_request_team_status(request_team_id=request_team_id, status=RequestStatus.FAIL)
    await db_model.set_request_team_comment(request_team_id=request_team_id, comment=comment)
    request_team = await db_model.get_request_team(request_team_id=request_team_id)

    team_player_captain = await db_model.get_captain_by_team_id(team_id=request_team.team_id)
    player = await db_model.get_player(player_id=team_player_captain.player_id)
    member = await db_model.get_member(member_id=player.member_id)

    message_text = '<b>Вы не прошли верификацию команды.</b>\n\n' \
                   'По причине:\n' \
                   f'{request_team.comment}'

    await notify_user(
        chat_id=member.user_id,
        text=message_text,
        bot=msg.bot
    )


def register_handlers_team_requests(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team_requests, text=["team_requests"], state="*", is_admin=True)
    dp.register_callback_query_handler(menu_view_all_team_requests, text=["view_all_team_requests"], state="*", is_admin=True)
    dp.register_callback_query_handler(menu_view_team_request, text_contains=["view_team_request"], state="*", is_admin=True)
    dp.register_callback_query_handler(moderation_team_request, text_contains=["moderation_team_request"], state="*", is_admin=True)
    dp.register_message_handler(enter_comment_team_request, state=VerifRequestTeam.ENTER_COMMENT_REQUEST_TEAM, is_admin=True)
