from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def menu_team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    player_kb = call.bot.get('kb').get('player')

    team_ikb = await player_kb.get_team_ikb()
    await call.message.answer('У вас ещё не команды.\n'
                              'Самое время это исправить.', reply_markup=team_ikb)


def register_handlers_menu_team(dp: Dispatcher):
    dp.register_callback_query_handler(menu_team, text=['team'], state='*', is_player=True)
