from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def matches(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    admin_kb = call.bot.get('kb').get('admin')

    matches_ikb = await admin_kb.get_matches_ikb()

    await call.message.answer('<b>Матч</b>\n\n'
                              'Выберите действие:',
                              reply_markup=matches_ikb)


async def add_match(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')


def register_handlers_matches(dp: Dispatcher):
    dp.register_callback_query_handler(matches, text=['matches'], state='*', is_admin=True)
