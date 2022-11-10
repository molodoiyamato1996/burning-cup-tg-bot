import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext


async def notify_user(text: str, chat_id: int, reply_markup=None, msg: types.Message = None, call: types.CallbackQuery = None,
                      state: FSMContext = None, time_out=None):
    bot = msg.bot if msg else call.bot

    if time_out:
        await asyncio.sleep(time_out)

    await bot.send_message(text=text, chat_id=chat_id, reply_markup=reply_markup)


async def notify_moderators(text: str, rule: str, kb=None,  msg: types.Message = None, call: types.CallbackQuery = None, state: FSMContext = None):
    bot = msg.bot if msg else call.bot
    db_model = bot.get('db_model')
    moderators = await db_model.get_moderators(rule=rule)

    if moderators is not None:
        for moderator in moderators:
            await bot.send_message(text=text, chat_id=moderator.user_id, reply_markup=kb)


