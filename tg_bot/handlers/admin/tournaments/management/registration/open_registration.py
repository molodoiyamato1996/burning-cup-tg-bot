import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.is_number import is_number
from tg_bot.misc.emoji import Emoji
from tg_bot.misc.notify import notify_user
from tg_bot.misc.scheduler import scheduler
from tg_bot.types.registration import StartRegistrationStates, RegistrationStatus


# дата начала
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

    current_date = datetime.datetime.now()

    # проверить является ли дата актуальной
    bot = msg.bot
    db_model = bot.get('db_model')
    tournament = await db_model.get_tournament()

    await db_model.add_registration(opening_date=opening_date, tournament_id=tournament.id)

    date_left = opening_date - current_date

    await msg.answer('<b>Регистрация успешно добавлена</b>\n\n'
                     f'Дата: <code>{opening_date}</code>\n'
                     f'До начала: <code>{date_left}</code>')

    team_player_kb = bot.get('kb').get('team_player')

    msg_text = f'<b> {Emoji.burn}Регистрация на турнир открыта</b>\n\n'
    participate_ikb = await team_player_kb.get_participate_ikb()

    date_left_in_second = date_left.total_seconds()
    teams = await db_model.get_teams_active()

    for team in teams:
        captain = await db_model.get_captain_by_team_id(team_id=team.id)
        player = await db_model.get_player_by_id(player_id=captain.id)
        member = await db_model.get_member_by_id(member_id=player.id)

        await scheduler(notify_user, date_left_in_second, bot, msg_text, participate_ikb, member.user_id)

    await scheduler(db_model.set_registration_status, date_left_in_second, RegistrationStatus.OPEN)

    await state.finish()


def register_handlers_start_registration(dp: Dispatcher):
    dp.register_callback_query_handler(start_registration, text=['start_registration'], state='*', is_admin=True)
    dp.register_message_handler(enter_date_registration, state=StartRegistrationStates.ENTER_START_DATE, is_admin=True)
