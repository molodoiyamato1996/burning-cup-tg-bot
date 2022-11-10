import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def view_registration(self, call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    registration = await db_model.get_registration()

    current_date = datetime.datetime.now()

    start = datetime.datetime.fromtimestamp(registration.opening_date)
    left = start - current_date if start > current_date else 'Регистрация уже началась'

    count_tournament_teams = len(await db_model.get_tournament_teams())

    free_places_left = registration.count_teams - count_tournament_teams if count_tournament_teams is not None else registration.limit_teams

    msg_text = f'<b>Просмотр регистрации</b>\n\n' \
               f'Кол-во мест: <code>{registration.limit_teams}</code>\n' \
               f'Свободных мест: <code>{free_places_left}</code>\n' \
               f'Дата начала: <code>{start}</code>\n' \
               f'До начала регистрации осталось: <code>{left}</code>'

    back_to_registration_ikb = await admin_kb.get_back_to_registration_ikb()

    await call.bot.edit_message_text(
        text=msg_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=back_to_registration_ikb
    )


def register_handlers_view_registration(dp: Dispatcher):
    dp.register_callback_query_handler(view_registration, text=['view_registration'], state='*', is_admin=True)
