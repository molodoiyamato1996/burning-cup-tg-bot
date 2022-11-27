from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team_player.states.set_fastcup import SetFastcup


async def set_fastcup(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    await call.message.answer('Введите новый фасткап:')
    await state.set_state(SetFastcup.ENTER_NEW_FASTCUP)


async def enter_new_fastcup(msg: types.Message, state=FSMContext):
    fastcup = msg.text.replace(' ', '')

    db_model = msg.bot.get('db_model')

    if await db_model.validation_player_fastcup(fastcup=fastcup):
        await msg.answer('Данный фасткап уже используется')
        return

    await db_model.set_player_fastcup(user_id=msg.from_user.id, fastcup=fastcup)
    await msg.answer('✅ Фасткап успешно изменён')
    await state.finish()


def register_handlers_set_fastcup(dp: Dispatcher):
    dp.register_callback_query_handler(set_fastcup, text=['set_fastcup'], state='*')
    dp.register_message_handler(enter_new_fastcup, state=SetFastcup.ENTER_NEW_FASTCUP)
