from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.moderator import VerifRequestMember
from tg_bot.types.request import RequestStatus
from tg_bot.types.member import MemberType
from ...misc.parse import parse_callback
from ...misc.notify import notify_user


async def view_request_member(call: types.CallbackQuery):
    await call.answer(' ')

    bot = call.bot
    db_model = bot.get('db_model')
    moderator_kb = bot.get('kb').get('moderator')

    call_data = call.data

    props = await parse_callback('view_request_member', call_data)

    request_member_user_id = props.get('user_id')

    request_member = await db_model.get_request_member(user_id=request_member_user_id)

    if request_member.request_member_status == RequestStatus.PROCESS:
        await call.message.answer('Анкета уже находится в процессе верификации')
        return
    elif request_member.request_member_status == RequestStatus.SUCCESS or request_member.request_member_status == RequestStatus.FAIL:
        await call.message.answer('Анкета уже рассмотрена!')
        await call.message.delete()
        return

    await db_model.set_request_member_status(user_id=request_member_user_id, status=RequestStatus.PROCESS)

    actions_verif_ikb = await moderator_kb.get_actions_verif_ikb(user_id=request_member_user_id)

    member_type = request_member.member_type

    student_msg_text = f'<b>Верификация студента.</b>\n\n' \
                   f'ФИО: {request_member.first_name} {request_member.last_name} {request_member.patronymic}\n' \
                   f'Учебное заведение: {request_member.institution}\n' \
                   f'Группа: {request_member.group}'
    schoolboy_msg_text = f'<b>Верификация школьника.</b>\n\n' \
                   f'ФИО: {request_member.first_name} {request_member.last_name} {request_member.patronymic}\n' \
                   f'Учебное заведение: {request_member.institution}\n' \
                   f'Класс: {request_member.group}'
    msg_text = student_msg_text if member_type == MemberType.STUDENT else schoolboy_msg_text
    await bot.send_photo(chat_id=call.message.chat.id, photo=request_member.document_photo,
                         caption=msg_text,
                         reply_markup=actions_verif_ikb)


async def verif_request_member(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')

    bot = call.bot
    db_model = bot.get('db_model')

    call_data = call.data

    props = await parse_callback('verif_request_member', call_data)

    request_member_user_id = props.get('user_id')
    request_member_result = props.get('result')

    if request_member_result == 'no':
        await call.message.answer('Введите причину отказа:')
        await state.set_state(VerifRequestMember.ENTER_RESPONSE)

        async with state.proxy() as data:
            data['user_id'] = request_member_user_id
    elif request_member_result == 'yes':
        await call.message.delete()
        await db_model.set_request_member_status(user_id=request_member_user_id, status=RequestStatus.SUCCESS)
        request_member = await db_model.get_request_member(user_id=request_member_user_id)
        await db_model.add_member(user_id=request_member.user_id, first_name=request_member.first_name,
                                  last_name=request_member.last_name, patronymic=request_member.patronymic,
                                  institution=request_member.institution, member_type=request_member.member_type,
                                  group=request_member.group)

        member_kb = call.bot.get('kb').get('member')

        create_player_ikb = await member_kb.get_create_player_ikb()

        await notify_user(bot=call.bot, text='<b>✅ Верификация успешно пройдена!</b>', chat_id=request_member_user_id,
                          reply_markup=create_player_ikb)


async def enter_comment_request_student(msg: types.Message, state=FSMContext):
    response_verif_request = msg.text

    state_data = await state.get_data()

    db_model = msg.bot.get('db_model')
    request_user_id = state_data.get('user_id')

    await db_model.set_request_member_status(user_id=request_user_id, status=RequestStatus.FAIL)
    await db_model.set_request_member_comment(user_id=request_user_id, comment=response_verif_request)
    user_kb = msg.bot.get('kb').get('user')
    repeated_request_member_ikb = await user_kb.get_repeated_request_member_ikb()
    await notify_user(bot=msg.bot, text=f'<b>❌ Вы не прошли верификацию</b>\n\n'
                                    f'<b>По причине:</b>\n{response_verif_request}', chat_id=request_user_id, reply_markup=repeated_request_member_ikb)

    await state.finish()


def register_handlers_verif_request_member(dp: Dispatcher):
    dp.register_callback_query_handler(view_request_member, text_contains=['view_request_member'])
    dp.register_callback_query_handler(verif_request_member, text_contains=['verif_request_member'], state='*')
    dp.register_message_handler(enter_comment_request_student, state=VerifRequestMember.ENTER_RESPONSE)
