from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.member.states.create_player import CreatePlayer


async def cmd_start_member(msg: types.Message, state=FSMContext):
    await state.finish()

    phrases = msg.bot.get('phrases')
    user_kb = msg.bot.get('kb').get('user')

    if msg.text != '💠 Меню':
        menu_kb = await user_kb.get_start_kb()
        await msg.answer('Добро пожаловать!', reply_markup=menu_kb)

    await msg.answer(text=phrases.second_step_registration)
    await state.set_state(CreatePlayer.ENTER_USERNAME)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start_member, commands=['start'], state='*', is_member=True)
    dp.register_message_handler(cmd_start_member, text='💠 Меню', state='*', is_member=True)
