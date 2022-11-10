from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.member.type import MemberType
from tg_bot.types.user.states.create_request_member import CreateRequestMember
from tg_bot.types.moderator.rule import ModeratorRule
from ...misc.notify import notify_moderators
from ...misc.parse import parse_callback
from tg_bot.types.user.institution.type import InstitutionType


async def choice_member_type(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')

    call_data = call.data
    user_kb = call.message.bot.get('kb').get('user')
    db_model = call.bot.get('db_model')

    props = await parse_callback('choice_member_type', call_data)

    member_type = props.get('member_type')

    async with state.proxy() as data:
        data['member_type'] = member_type

    institution_type = InstitutionType.COLLEGE if member_type == MemberType.STUDENT else InstitutionType.SCHOOL

    institutions = await db_model.get_institutions(institution_type=institution_type)

    institution_ikb = await user_kb.get_choice_institution_ikb(institutions=institutions)

    await call.message.answer('<b>Выберите Ваше учебное заведение:</b>', reply_markup=institution_ikb)
    await CreateRequestMember.next()


async def choice_institution(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.answer('')

    phrases = call.bot.get('phrases')
    db_model = call.bot.get('db_model')

    call_data = call.data

    props = await parse_callback('choice_institution', call_data)

    institution_id = props.get('id')
    institution_type = props.get('type')

    institution = await db_model.get_institution(institution_id=institution_id, institution_type=institution_type)

    async with state.proxy() as data:
        data['institution'] = institution.name

    await call.message.answer(phrases.enter_fullname)
    await CreateRequestMember.next()


async def enter_fullname(msg: types.Message, state=FSMContext):
    fullname = msg.text

    for s in fullname:
        if s.isdigit():
            await msg.answer('<b>❌ Сообщение не должно содержать цифры!</b>\n\n'
                             '✅ Например: Иванов Иван Иванович')
            return

    fullname_data = fullname.split(' ')

    if len(fullname_data) != 3:
        await msg.answer('<b>❌ Введите полные данные!</b>\n\n'
                         '✅ Например: Иванов Иван Иванович')
        return

    async with state.proxy() as data:
        data['first_name'] = fullname_data[0].capitalize()
        data['last_name'] = fullname_data[1].capitalize()
        data['patronymic'] = fullname_data[2].capitalize()

    state_data = await state.get_data()
    member_type = state_data.get('member_type')

    student_text = '<b>Введите Вашу группу:</b>\n\n' \
                   '✅ Например: Д192/2'
    schoolboy_text = '<b>Введите Ваш класс:</b>\n\n' \
                     '✅ Например: 9А'
    message_text = student_text if member_type == MemberType.STUDENT else schoolboy_text

    await msg.answer(message_text)

    await CreateRequestMember.next()


async def enter_group(msg: types.Message, state=FSMContext):
    group = msg.text.upper()

    async with state.proxy() as data:
        data['group'] = group

    state_data = await state.get_data()
    member_type = state_data.get('member_type')

    student_text = '📷 Отправьте фото Вашего студенческого'
    schoolboy_text = '📷 Отправьте фото Вашего документа удостоверяющего личность'
    message_text = student_text if member_type == MemberType.STUDENT else schoolboy_text

    await msg.answer(message_text)
    await CreateRequestMember.next()


async def send_document_photo(msg: types.Message, state=FSMContext):
    document_photo = msg.photo[-1].file_id
    user_id = msg.from_user.id

    db_model = msg.bot.get('db_model')
    moderator_kb = msg.bot.get('kb').get('moderator')
    state_data = await state.get_data()

    first_name = state_data.get('first_name')
    last_name = state_data.get('last_name')
    patronymic = state_data.get('patronymic')
    group = state_data.get('group')
    member_type = state_data.get('member_type')
    institution = state_data.get('institution')

    await db_model.add_request_member(user_id=user_id, first_name=first_name, last_name=last_name,
                                      patronymic=patronymic, group=group, document_photo=document_photo,
                                      institution=institution, member_type=member_type)

    ib_viewing_verif_request = await moderator_kb.get_view_verif_request_ikb(user_id=user_id)

    await notify_moderators(text='<b>🛎 Появилась новая анкета</b>', msg=msg, rule=ModeratorRule.VERIF_STUDENT,
                            kb=ib_viewing_verif_request)
    await msg.answer(text='<b>✅ Ваша анкета отправлена на рассмотрение!</b>\n\n'
                          '🛎 Ожидайте уведомления!')
    await state.finish()


def register_handlers_create_member(dp: Dispatcher):
    dp.register_callback_query_handler(choice_member_type, state=CreateRequestMember.CHOICE_MEMBER_TYPE)
    dp.register_callback_query_handler(choice_institution, state=CreateRequestMember.CHOICE_EDUCATIONAL_INSTITUTION)
    dp.register_message_handler(enter_fullname, state=CreateRequestMember.ENTER_FULLNAME)
    dp.register_message_handler(enter_group, state=CreateRequestMember.ENTER_GROUP)
    dp.register_message_handler(send_document_photo, state=CreateRequestMember.SEND_DOCUMENT_PHOTO,
                                content_types=types.ContentType.PHOTO)
