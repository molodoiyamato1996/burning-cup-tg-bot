from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team_player.states.set_username import SetUsername


async def set_username(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    await call.message.answer('Введите новый псевдоним:')
    await state.set_state(SetUsername.ENTER_NEW_USERNAME)


async def enter_new_username(msg: types.Message, state=FSMContext):
    username = msg.text.replace(' ', '')

    db_model = msg.bot.get('db_model')

    if await db_model.validation_player_username(username=username):
        await msg.answer('Данный псевдоним уже используется')
        return

    await db_model.set_player_username(user_id=msg.from_user.id, username=username)
    await msg.answer('✅ Псевдоним успешно изменён')
    await state.finish()


def register_handlers_set_username(dp: Dispatcher):
    dp.register_callback_query_handler(set_username, text=['set_username'], state='*')
    dp.register_message_handler(enter_new_username, state=SetUsername.ENTER_NEW_USERNAME)
