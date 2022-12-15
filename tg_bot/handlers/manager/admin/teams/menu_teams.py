from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.sctripts import parse_callback
from tg_bot.misc.phares import Phrases


async def menu_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')
    db_model = call.bot.get('db_model')

    teams = await db_model.get_teams()

    if len(teams) == 0:
        answer_text = Phrases.teams_title + 'Ещё ни одна команда не зарегистрирована'

        await call.message.answer(
            text=answer_text,
        )
        return

    team_ikb = await admin_kb.get_menu_teams_ikb(teams=teams)

    answer_text = Phrases.teams_title

    await call.message.answer(
        text=answer_text,
        reply_markup=team_ikb
    )


async def view_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    props = await parse_callback("view_team", call.data)

    team_id = props.get("team_id")

    admin_kb = call.bot.get("kb").get("admin")

    db_model = call.bot.get("db_model")

    team = await db_model.get_team(team_id=team_id)

    team_players = await db_model.get_team_players_by_team_id(team_id=team_id)

    players = []
    captain = None

    for team_player in team_players:
        if team_player.is_captain:
            captain = await db_model.get_player(player_id=team_player.player_id)
        else:
            players.append(await db_model.get_player(player_id=team_player.player_id))

    view_team_ikb = await admin_kb.get_view_team_ikb(players=players, captain=captain, team_id=team_id)

    caption = "<b>Просмотр команды</b>\n\n" \
              f"Название команды: <code>{team.name}</code>\n" \
              "Состав команды:"

    await call.bot.send_photo(
        chat_id=call.from_user.id,
        photo=team.photo_telegram_id,
        caption=caption,
        reply_markup=view_team_ikb
    )


def register_handlers_menu_teams(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team, text=["teams"], state='*')
    dp.register_callback_query_handler(view_team, text_contains=["view_team"], state='*')
