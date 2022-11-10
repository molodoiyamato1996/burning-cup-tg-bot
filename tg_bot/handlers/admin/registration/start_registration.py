import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.is_number import is_number
from tg_bot.misc.emoji import Emoji
from tg_bot.misc.notify import notify_user

from tg_bot.types.registration.states import StartRegistrationStates


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

    opening_date = datetime.datetime(day=int(data_date[0]), month=int(data_date[1]), year=int(data_date[2]),
                                   hour=int(data_time[0]),
                                   minute=int(data_time[1]))
    opening_date_in_seconds = opening_date.timestamp()

    async with state.proxy() as data:
        data['opening_date_in_seconds'] = opening_date_in_seconds

    msg_text = 'Введите ограничение по количеству команд:'
    await msg.answer(text=msg_text)
    await StartRegistrationStates.next()


async def enter_count_team(msg: types.Message, state=FSMContext):
    msg_text = msg.text

    limit_teams = await is_number(value=msg_text)

    if limit_teams is None:
        await msg.answer('Введите корректное число')
        return

    db_model = msg.bot.get('db_model')
    team_player_kb = msg.bot.get('kb').get('team_player')

    state_data = await state.get_data()

    opening_date_in_seconds = state_data.get('opening_date_in_seconds')
    await db_model.add_registration(opening_date=opening_date_in_seconds, limit_teams=limit_teams)

    current_date = datetime.datetime.now()

    opening_date = datetime.datetime.fromtimestamp(opening_date_in_seconds)
    left = opening_date - current_date if opening_date > current_date else 'Регистрация уже началась'

    current_date_in_second = datetime.datetime.now().timestamp()
    date_left_in_second = opening_date_in_seconds - current_date_in_second

    await msg.answer('<b>Регистрация успешно добавлена</b>\n\n'
                     f'Кол-во команд: <code>{limit_teams}</code>\n'
                     f'Дата: <code>{opening_date}</code>\n'
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


def register_handlers_start_registration(dp: Dispatcher):
    dp.register_callback_query_handler(start_registration, text=['start_registration'], state='*', is_admin=True)
    dp.register_message_handler(enter_date_registration, state=StartRegistrationStates.ENTER_START_DATE, is_admin=True)
    dp.register_message_handler(enter_count_team, state=StartRegistrationStates.ENTER_COUNT_TEAMS, is_admin=True)
