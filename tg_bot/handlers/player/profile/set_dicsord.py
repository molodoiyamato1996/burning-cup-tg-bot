from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tg_bot.types.team_player import SetDiscord
from tg_bot.types.request import RequestStatus
from tg_bot.misc.phares import Phrases


async def set_discrod(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.answer(' ')

    db_model = call.bot.get('db_model')

    team_player = await db_model.get_team_player(user_id=call.from_user.id)

    if team_player:
        request_team = await db_model.get_request_team_by_team_id(team_id=team_player.team_id)

        if request_team:
            if request_team.request_team_status == RequestStatus.WAIT or request_team.request_team_status == RequestStatus.PROCESS:
                answer_text = Phrases.team_player_verification_block
                await call.message.answer(answer_text)
                return

    answer_text = Phrases.enter_new_discord

    await call.message.answer(answer_text)
    await state.set_state(SetDiscord.ENTER_NEW_DISCORD)


async def enter_new_discord(msg: types.Message, state=FSMContext):
    discord = msg.text.replace(' ', '')

    db_model = msg.bot.get('db_model')

    if await db_model.validation_player_discord(discord=discord):
        answer_text = Phrases.discord_already_in_use

        await msg.answer(answer_text)
        return

    await db_model.set_player_discord(user_id=msg.from_user.id, discord=discord)

    answer_text = Phrases.discord_success_changed

    await msg.answer(answer_text)
    await state.finish()


def register_handlers_set_discord(dp: Dispatcher):
    dp.register_callback_query_handler(set_discrod, text=['set_discord'], state='*', is_player=True)
    dp.register_message_handler(enter_new_discord, state=SetDiscord.ENTER_NEW_DISCORD, is_player=True)