import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.is_number import is_number
from tg_bot.misc.emoji import Emoji
from tg_bot.misc.notify import notify_user
from tg_bot.types.registration.status import RegistrationStatus
from tg_bot.types.registration.states import StartRegistrationStates


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


async def view_registration(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')
    admin_kb = call.bot.get('kb').get('admin')

    registration = await db_model.get_registration()

    current_date = datetime.datetime.now()

    start = datetime.datetime.fromtimestamp(registration.start_date)
    left = start - current_date if start > current_date else 'Регистрация уже началась'

    count_tournament_teams = len(await db_model.get_tournament_teams())

    free_places_left = registration.count_teams - count_tournament_teams if count_tournament_teams is not None else registration.count_teams

    msg_text = f'<b>Просмотр регистрации</b>\n\n' \
               f'Кол-во команд: <code>{registration.count_teams}</code>\n' \
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


async def cancel_registration(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')

    registration = await db_model.get_registration()

    await db_model.set_registration_status(registration_id=registration.id, status=RegistrationStatus.CANCEL)
    await call.bot.edit_message_text(
        text='Регистрация успешно отменена',
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )


async def start_registration(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    msg_text = 'Напишити дату и время начала регистрации:' \
               'В формате day:month:year@hour:minute'

    await call.message.answer(text=msg_text)
    await state.set_state(StartRegistrationStates.ENTER_START_DATE)


async def enter_date_registration(msg: types.Message, state=FSMContext):
    msg_text = msg.text

    if not msg_text:
        return msg.answer('Введите корректную дату')

    date_and_time = msg_text.split('@')

    data_date = date_and_time[0].split(':')
    data_time = date_and_time[1].split(':')

    start_date = datetime.datetime(day=int(data_date[0]), month=int(data_date[1]), year=int(data_date[2]),
                                   hour=int(data_time[0]),
                                   minute=int(data_time[1]))
    start_date_in_seconds = start_date.timestamp()
    print(start_date_in_seconds)

    async with state.proxy() as data:
        data['start_date'] = start_date_in_seconds

    msg_text = 'Введите количество команд:'
    await msg.answer(text=msg_text)
    await StartRegistrationStates.next()


async def enter_count_team(msg: types.Message, state=FSMContext):
    msg_text = msg.text

    count_teams = await is_number(value=msg_text)

    if count_teams is None:
        await msg.answer('Введите корректное число')
        return

    db_model = msg.bot.get('db_model')
    team_player_kb = msg.bot.get('kb').get('team_player')

    state_data = await state.get_data()

    start_date_in_second = state_data.get('start_date')
    await db_model.add_registration(start_date=start_date_in_second, count_teams=count_teams)

    current_date = datetime.datetime.now()

    start = datetime.datetime.fromtimestamp(start_date_in_second)
    left = start - current_date if start > current_date else 'Регистрация уже началась'

    current_date_in_second = datetime.datetime.now().timestamp()
    date_left_in_second = start_date_in_second - current_date_in_second

    await msg.answer('<b>Регистрация успешно добавлена</b>\n\n'
                     f'Кол-во команд: <code>{count_teams}</code>\n'
                     f'Дата: <code>{start}</code>\n'
                     f'Осталось: <code>{left}</code>')

    msg_text = f'<b> {Emoji.burn}Регистрация на турнир открыта</b>\n\n'
    participate_ikb = await team_player_kb.get_participate_ikb()

    await state.finish()

    teams = await db_model.get_teams_active()

    for team in teams:
        captain = await db_model.get_captain_by_team_id(team_id=team.id)
        player = await db_model.get_player_by_id(player_id=captain.id)
        member = await db_model.get_member_by_id(member_id=player.id)
        await notify_user(time_out=date_left_in_second, msg=msg, text=msg_text, reply_markup=participate_ikb, chat_id=member.user_id)




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


def register_handlers_registration(dp: Dispatcher):
    dp.register_callback_query_handler(registration, text=['registration'], state='*', is_admin=True)
    dp.register_callback_query_handler(cancel_registration, text=['cancel_registration'], state='*', is_admin=True)
    dp.register_callback_query_handler(view_registration, text=['view_registration'], state='*', is_admin=True)
    dp.register_callback_query_handler(start_registration, text=['start_registration'], state='*', is_admin=True)
    dp.register_callback_query_handler(back_to_registration, text=['back_to_registration'], state='*', is_admin=True)
    dp.register_message_handler(enter_date_registration, state=StartRegistrationStates.ENTER_START_DATE, is_admin=True)
    dp.register_message_handler(enter_count_team, state=StartRegistrationStates.ENTER_COUNT_TEAMS, is_admin=True)
