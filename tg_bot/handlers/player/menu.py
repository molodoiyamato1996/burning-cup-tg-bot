from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.types.team_player.status import TeamPlayerStatus


async def profile(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')
    player_kb = call.bot.get('kb').get('player')
    player = await db_model.get_player(user_id=call.from_user.id)

    profile_ikb = await player_kb.get_profile_ikb()

    if await db_model.team_player_exist(user_id=call.from_user.id):
        team_player = await db_model.get_team_player(user_id=call.from_user.id)
        team = await db_model.get_team(team_id=team_player.team_id)
        message_text = '<b>👤 Профиль</b>\n\n' \
                       f'<b>Команда</b>: <code>{team.name}</code>\n' \
                       f'<b>Псевдоним</b>: <code>{player.username}</code>\n' \
                       f'<b>Дискорд</b>: <code>{player.discord}</code>\n' \
                       f'<b>Фасткап</b>: <code>{player.fastcup}</code>'
    else:
        message_text = '<b>👤 Профиль</b>\n\n' \
                       f'<b>Псевдоним</b>: <code>{player.username}</code>\n' \
                       f'<b>Дискорд</b>: <code>{player.discord}</code>\n' \
                       f'<b>Фасткап</b>: <code>{player.fastcup}</code>'

    await call.bot.edit_message_text(
        text=message_text,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=profile_ikb
    )


async def team(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    player_kb = call.bot.get('kb').get('player')

    team_ikb = await player_kb.get_team_ikb()
    await call.message.answer('У вас ещё не команды.\n'
                              'Самое время это исправить.', reply_markup=team_ikb)


async def rules(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')


async def support(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')


def register_handlers_menu(dp: Dispatcher):
    dp.register_callback_query_handler(profile, text=['profile'], state='*', is_player=True)
    dp.register_callback_query_handler(team, text=['team'], state='*', is_player=True)
    dp.register_callback_query_handler(rules, text=['rules'], state='*', is_player=True)
    dp.register_callback_query_handler(support, text=['support'], state='*', is_player=True)
