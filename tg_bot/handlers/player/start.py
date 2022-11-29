from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.player.status import PlayerStatus


async def cmd_start_player(msg: types.Message, state=FSMContext):
    await state.finish()

    bot = msg.bot
    user_id = msg.from_user.id
    db_model = bot.get('db_model')
    user_kb = bot.get('kb').get('user')
    player_kb = bot.get('kb').get('player')
    phrases = bot.get('phrases')

    if msg.text != '💠 Меню':
        menu_kb = await user_kb.get_start_kb()
        await msg.answer('Добро пожаловать!', reply_markup=menu_kb)

    player = await db_model.get_player(user_id=user_id)

    if player.player_status == PlayerStatus.BANNED:
        # Инлайн клавиатура с кнопкой обжаловать
        message_text = phrases.player_banned + player.comment
        await msg.answer(message_text)
    elif player.player_status == PlayerStatus.ACTIVE:
        menu_ikb = await player_kb.get_menu_ikb()
        await msg.answer(text=phrases.menu, reply_markup=menu_ikb)


async def back_to_menu(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()

    user_id = call.from_user.id
    db_model = call.bot.get('db_model')
    player_kb = call.bot.get('kb').get('player')
    phrases = call.bot.get('phrases')

    player = await db_model.get_player(user_id=user_id)

    if player.player_status == PlayerStatus.BANNED:
        # Инлайн клавиатура с кнопкой обжаловать
        message_text = phrases.player_banned + player.comment
        await call.message.answer(message_text)
    elif player.player_status == PlayerStatus.ACTIVE:
        menu_ikb = await player_kb.get_menu_ikb()
        await call.message.answer(text=phrases.menu, reply_markup=menu_ikb)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start_player, commands=['start'], state='*', is_player=True)
    dp.register_message_handler(cmd_start_player, text='💠 Меню', state='*', is_player=True)
    dp.register_callback_query_handler(back_to_menu, text=['back_to_menu'], state='*', is_player=True)
