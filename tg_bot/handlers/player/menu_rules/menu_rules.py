from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def menu_rules(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()


def register_handlers_menu(dp: Dispatcher):
    dp.register_callback_query_handler(menu_rules, text=['menu_rules'], state='*', is_player=True)
