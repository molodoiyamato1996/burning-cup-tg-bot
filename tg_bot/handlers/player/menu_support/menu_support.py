from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def support(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')


def register_handlers_support(dp: Dispatcher):
    dp.register_callback_query_handler(support, text=['support'], state='*', is_player=True)
