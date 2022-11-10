from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.member.states.create_player import CreatePlayer


async def enter_username(msg: types.Message, state=FSMContext):
    username = msg.text

    db_model = msg.bot.get('db_model')
    phrases = msg.bot.get('phrases')

    if await db_model.validation_player_username(username=username):
        await msg.answer(text=phrases.error_username_already_taken)
        return

    async with state.proxy() as data:
        data['username'] = username

    await msg.answer(text=phrases.enter_discrod)
    await CreatePlayer.next()


async def enter_discord(msg: types.Message, state=FSMContext):
    discord = msg.text

    db_model = msg.bot.get('db_model')
    phrases = msg.bot.get('phrases')

    if '#' not in discord:
        await msg.answer(text=phrases.error_enter_correct_discrod)
        return
    if await db_model.validation_player_discord(discord=discord):
        await msg.answer(text=phrases.error_discrod_already_taken)
        return

    async with state.proxy() as data:
        data['discord'] = discord

    await msg.answer(text=phrases.enter_fastcup)
    await CreatePlayer.next()


async def enter_fastcup(msg: types.Message, state=FSMContext):
    fastcup = msg.text

    user_id = msg.from_user.id
    db_model = msg.bot.get('db_model')
    user_kb = msg.bot.get('kb').get('user')
    phrases = msg.bot.get('phrases')

    if await db_model.validation_player_fastcup(fastcup=fastcup):
        await msg.answer(text=phrases.error_fastcup_already_taken)
        return

    state_data = await state.get_data()

    username = state_data.get('username')
    discord = state_data.get('discord')

    await db_model.add_player(user_id=user_id, username=username, discord=discord, fastcup=fastcup)

    menu_ikb = await user_kb.get_menu_ikb()
    await msg.answer(text=phrases.menu, reply_markup=menu_ikb)
    await state.finish()


def register_handlers_create_player(dp: Dispatcher):
    dp.register_message_handler(enter_username, state=CreatePlayer.ENTER_USERNAME, is_member=True)
    dp.register_message_handler(enter_discord, state=CreatePlayer.ENTER_DISCORD, is_member=True)
    dp.register_message_handler(enter_fastcup, state=CreatePlayer.ENTER_FASCTCUP, is_member=True)