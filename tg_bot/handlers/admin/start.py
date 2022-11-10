from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.misc.emoji import Emoji


async def start(msg: types.Message, state=FSMContext):
    await state.finish()

    admin_kb = msg.bot.get('kb').get('admin')

    start_ikb = await admin_kb.get_start_ikb()

    msg_text = f'<b>{Emoji.burn} Добро пожаловать администратор</b>\n\n' \
                     f'Выберите действие:'

    await msg.answer(text=msg_text,
                     reply_markup=start_ikb)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], is_admin=True)
