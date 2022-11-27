from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.captain import SetTeamName
from tg_bot.misc.parse import parse_callback


async def set_team_name(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await state.finish()

    props = await parse_callback('set_team_name', call.data)
    team_id = props.get('team_id')

    await call.message.answer('Введите новое имя команды:')
    await state.set_state(SetTeamName.ENTER_NEW_TEAM_NAME)
    async with state.proxy() as data:
        data['team_id'] = team_id


async def enter_new_team_name(msg: types.Message, state=FSMContext):
    new_team_name = msg.text

    db_model = msg.bot.get('db_model')

    state_data = await state.get_data()
    team_id = state_data.get('team_id')

    if await db_model.is_valid_team_name(name=new_team_name):
        await msg.answer('Такое название уже используется.')
        return

    await db_model.set_team_name(team_id=team_id, name=new_team_name)

    await msg.answer('Вы успешно изменили название команды.')

    await state.finish()


def register_handlers_set_team_name(dp: Dispatcher):
    dp.register_callback_query_handler(set_team_name, text_contains=['set_team_name'], state='*')
    dp.register_message_handler(enter_new_team_name, state=SetTeamName.ENTER_NEW_TEAM_NAME)
