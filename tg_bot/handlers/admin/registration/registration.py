from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.registration.status import RegistrationStatus


async def registration(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    registration = await db_model.get_registration()

    if registration is None:
        is_registration = False
    else:
        is_registration = True if registration.registration_status == RegistrationStatus.OPEN else False

    registration_ikb = await admin_kb.get_registration_ikb(is_registration=is_registration)

    await call.message.answer(text='<b>Регистрации</b>\n\n'
                                   'Выберите действие:',
                              reply_markup=registration_ikb)


async def back_to_registration(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    registration = await db_model.get_registration()

    if registration is None:
        is_registration = False
    else:
        is_registration = True if registration.registration_status == RegistrationStatus.OPEN else False

    registration_ikb = await admin_kb.get_registration_ikb(is_registration=is_registration)

    await call.bot.edit_message_text(
        text='<b>Регистрации</b>\n\n'
             'Выберите действие:',
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=registration_ikb)


def register_handlers_menu_registration(dp: Dispatcher):
    dp.register_callback_query_handler(registration, text=['registration'], state='*', is_admin=True)
    dp.register_callback_query_handler(back_to_registration, text=['back_to_registration'], state='*', is_admin=True)
