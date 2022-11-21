from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


async def participate(call: types.CallbackQuery, state=FSMContext):
    await call.answer(' ')
    await state.finish()




def register_handlers_participate(dp: Dispatcher):
    pass
