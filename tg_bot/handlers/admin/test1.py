# from aiogram import Dispatcher, types
# from aiogram.dispatcher import FSMContext
#
#
# async def get_all_team(msg: types.Message, state=FSMContext):
#     await state.finish()
#
#     db_model = msg.bot.get('db_model')
#     admin_kb = msg.bot.get('kb').get('admin')
#
#     tournament_teams = await db_model.get_tournament_teams()
#
#     view_tournament_teams_ikb = await admin_kb.get_view_tournament_teams_ikb(tournament_teams=tournament_teams)
#
#     if tournament_teams:
#         await msg.answer(text='<b>Команды турнира</b>',
#                          reply_markup=view_tournament_teams_ikb)
#         return
#
#     await msg.answer('Пока не зарегистрировано ни одной турнирной команды')
#
#
# def register_handlers_get_team(dp: Dispatcher):
#     dp.register_message_handler(get_all_team, commands=['get_all_team'], is_admin=True)
