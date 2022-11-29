from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.phares import Phrases


async def cmd_start_member(msg: types.Message, state=FSMContext):
    await state.finish()

    user_kb = msg.bot.get('kb').get('user')

    if msg.text != '💠 Меню':
        menu_kb = await user_kb.get_start_kb()
        await msg.answer('Добро пожаловать!', reply_markup=menu_kb)

    member_kb = msg.bot.get('kb').get('member')

    create_player_ikb = await member_kb.get_create_player_ikb()

    answer_text = Phrases.you_need_to_register_to_continue
    await msg.answer(answer_text, reply_markup=create_player_ikb)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start_member, commands=['start'], state='*', is_member=True)
    dp.register_message_handler(cmd_start_member, text='💠 Меню', state='*', is_member=True)
