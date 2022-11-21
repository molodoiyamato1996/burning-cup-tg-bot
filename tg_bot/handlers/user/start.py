from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.user.create_request_member import CreateRequestMember
from tg_bot.types.request.status import RequestStatus


async def cmd_start(msg: types.Message, state=FSMContext):
    await state.finish()

    user_id = msg.from_user.id
    db_model = msg.bot.get('db_model')
    user_kb = msg.bot.get('kb').get('user')
    phrases = msg.bot.get('phrases')

    if not await db_model.user_exist(user_id=user_id):
        await db_model.add_user(user_id=user_id, username=msg.from_user.username)

    if msg.text != '💠 Меню':
        menu_kb = await user_kb.get_start_kb()
        await msg.answer('Добро пожаловать!', reply_markup=menu_kb)

    if not await db_model.request_member_exist(user_id=user_id):
        choice_member_type_ikb = await user_kb.get_choice_member_type_ikb()
        await msg.answer(text=phrases.first_step_registration, reply_markup=choice_member_type_ikb)
        await state.set_state(CreateRequestMember.CHOICE_MEMBER_TYPE)
        return

    request_member = await db_model.get_request_member(user_id=user_id)

    if request_member.request_member_status == RequestStatus.FAIL:
        # Инлайн клавиатура с кнопки подавать новую заявку
        repeated_request_member_ikb = await user_kb.get_repeated_request_member_ikb()
        message_text = phrases.request_member_fail + request_member.comment
        await msg.answer(message_text, reply_markup=repeated_request_member_ikb)
    elif request_member.request_member_status == RequestStatus.PROCESS:
        await msg.answer(phrases.request_member_wait)
    elif request_member.request_member_status == RequestStatus.WAIT:
        await msg.answer(phrases.request_member_wait)


async def repeated_request_member(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    user_kb = call.bot.get('kb').get('user')
    phrases = call.bot.get('phrases')

    choice_member_type_ikb = await user_kb.get_choice_member_type_ikb()
    await call.message.answer(text=phrases.first_step_registration, reply_markup=choice_member_type_ikb)
    await state.set_state(CreateRequestMember.CHOICE_MEMBER_TYPE)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state='*', is_member=False)
    dp.register_message_handler(cmd_start, text='💠 Меню', state='*', is_member=False)
    dp.register_callback_query_handler(repeated_request_member, text=['repeated_request_member'], state='*', is_member=False)
