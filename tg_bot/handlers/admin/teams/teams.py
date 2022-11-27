from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.parse import parse_callback


async def tournament_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')

    team_ikb = await admin_kb.get_team_ikb()

    msg_text = f'<b>Команды турнира</b>\n\n' \
               'Выберите действие:'

    await call.message.answer(
        text=msg_text,
        reply_markup=team_ikb
    )


async def view_tournament_teams(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    tournament_teams = await db_model.get_tournament_teams()

    msg_text = f'<b>Команды турнира</b>'

    if len(tournament_teams) == 0:
        msg_text = f'<b>Команды турнира</b>\n\n' \
                   f'Ещё не одна команда не зарегистрировалась на турнире'
        await call.message.answer(
            text=msg_text
        )
        return

    view_tournament_team_ikb = await admin_kb.get_view_tournament_team_ikb(tournament_teams=tournament_teams)

    await call.message.answer(
        text=msg_text,
        reply_markup=view_tournament_team_ikb
    )


async def view_tournament_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')

    props = await parse_callback('view_tournament_team', callback_data=call.data)

    tournament_team_id = props.get('tournament_team_id')

    tournament_team = await db_model.get_tournament_team_by_id(tournament_team_id=tournament_team_id)

    msg_text = f'<b>Команда турнира</b>\n\n' \
               f'Название: <code>{tournament_team.name}</code>\n' \
               f'Статус команды: <code>{tournament_team.tournament_team_status}</code>'

    await call.bot.send_photo(
        chat_id=call.message.chat.id,
        photo=tournament_team.photo,
        caption=msg_text,

    )


async def block_team(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    msg_text = f'<b>Конанды турнира</b>\n\n' \
               f'Блокировка команды'

    await call.message.answer(
        text=msg_text
    )


def register_handlers_teams(dp: Dispatcher):
    dp.register_callback_query_handler(tournament_team, text=['teams'], state='*')
    dp.register_callback_query_handler(view_tournament_teams, text=['view_teams'], state='*')
    dp.register_callback_query_handler(view_tournament_team, text_contains=['view_team?'], state='*')
