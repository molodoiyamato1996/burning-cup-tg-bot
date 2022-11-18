from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def menu_days(call: types.CallbackQuery, state: FSMContext):
    await call.answer(' ')
    await state.finish()

    admin_kb = call.bot.get('kb').get('admin')

    day_title = '<b>День</b>\n\n'
    text = 'Выберите действие:'
    msg_text = day_title + text

    menu_days_ikb = await admin_kb.get_menu_days_ikb()
    await call.message.answer(text=msg_text,
                              reply_markup=menu_days_ikb)


def register_handlers_menu_days(dp: Dispatcher):
    dp.register_callback_query_handler(menu_days, text=[''], state='*')
