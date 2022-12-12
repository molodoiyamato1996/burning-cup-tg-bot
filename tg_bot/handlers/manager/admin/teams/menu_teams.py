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

    db_model = call.bot.get('db_model')


def register_handlers_menu_teams(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team, text=['teams'], state='*')
