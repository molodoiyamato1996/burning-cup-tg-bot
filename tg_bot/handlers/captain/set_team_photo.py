from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.captain import SetTeamPhoto
from tg_bot.misc.parse import parse_callback
from tg_bot.types.request import RequestStatus


async def set_team_photo(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await state.finish()

    props = await parse_callback('set_team_photo', call.data)
    team_id = props.get('team_id')
    db_model = call.bot.get('db_model')

    request_team = await db_model.get_request_team_by_team_id(team_id=team_id)

    if request_team:
        if request_team.request_team_status == RequestStatus.WAIT or request_team.request_team_status == RequestStatus.PROCESS:
            answer_text = 'Во время верификации команды, менять название или изображение команды запрещено'
            await call.message.answer(answer_text)
            return

    answer_text = 'Отправьте новое фото команды:'
    await call.message.answer(answer_text)
    await state.set_state(SetTeamPhoto.SEND_NEW_TEAM_PHOTO)
    async with state.proxy() as data:
        data['team_id'] = team_id


async def send_new_team_photo(msg: types.Message, state=FSMContext):
    new_team_photo = msg.photo[-1].file_id

    db_model = msg.bot.get('db_model')

    state_data = await state.get_data()
    team_id = state_data.get('team_id')

    await db_model.set_team_photo(team_id=team_id, photo=new_team_photo)

    await msg.answer('Вы успешно изменили фотографию команды.')

    await state.finish()


def register_handlers_set_team_photo(dp: Dispatcher):
    dp.register_callback_query_handler(set_team_photo, text_contains=['set_team_photo'], state='*')
    dp.register_message_handler(send_new_team_photo, state=SetTeamPhoto.SEND_NEW_TEAM_PHOTO, content_types=types.ContentType.PHOTO)