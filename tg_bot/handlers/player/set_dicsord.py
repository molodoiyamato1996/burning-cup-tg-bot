from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team_player.states.set_discord import SetDiscord


async def set_discrod(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    await call.message.answer('Введите новый дискорд:')
    await state.set_state(SetDiscord.ENTER_NEW_DISCORD)


async def enter_new_discord(msg: types.Message, state=FSMContext):
    discord = msg.text.replace(' ', '')

    db_model = msg.bot.get('db_model')

    if await db_model.validation_player_discord(discord=discord):
        await msg.answer('Данный дискорд уже используется')
        return

    await db_model.set_player_discord(user_id=msg.from_user.id, discord=discord)
    await msg.answer('✅ Дискорд успешно изменён')
    await state.finish()


def register_handlers_set_discord(dp: Dispatcher):
    dp.register_callback_query_handler(set_discrod, text=['set_discord'], state='*')
    dp.register_message_handler(enter_new_discord, state=SetDiscord.ENTER_NEW_DISCORD)