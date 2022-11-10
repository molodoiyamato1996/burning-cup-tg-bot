import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tg_bot.config import load_config

from tg_bot.filters.admin import AdminFilter
from tg_bot.filters.member import MemberFilter
from tg_bot.filters.player import PlayerFilter
from tg_bot.filters.team_player import TeamPlayerFilter
from tg_bot.filters.captain import CaptainFilter

from tg_bot.models.db_model.db_interaction import DBInteraction
from tg_bot.models.db_model import Base

from tg_bot.keyboards import kb

from tg_bot.handlers import register_all_handlers

from tg_bot.types.user.institution.type import InstitutionType
from tg_bot.misc.phares import Phrases

from data import schools, colleges


logger = logging.getLogger(__name__)


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(MemberFilter)
    dp.filters_factory.bind(PlayerFilter)
    dp.filters_factory.bind(TeamPlayerFilter)
    dp.filters_factory.bind(CaptainFilter)


async def add_institutions(db):
    for school in schools:
        await db.add_institution(name=school, institution_type=InstitutionType.SCHOOL)

    for college in colleges:
        await db.add_institution(name=college, institution_type=InstitutionType.COLLEGE)


async def test_configuration(db, admin_id: int):
    await add_admin_data(db, admin_id=admin_id)
    await add_test_team(db)


async def add_admin_data(db, admin_id: int):
    user = await db.add_user(user_id=admin_id, username='skywalker')
    await db.add_moderator(user_id=admin_id, rule='ALL')
    await db.add_member(
        user_id=user.id,
        last_name='Иванов',
        first_name='Иван',
        patronymic='Иванович',
        institution='СПК',
        group='Д192/2',
        member_type='STUDENT'
    )
    await db.add_player(user_id=user.id, username='skywalker', discord='skywalker#1234', fastcup='skywalker')


async def add_test_team(db, admin_id: int):
    await add_admin_data(db, admin_id)

    team = await db.add_team(
        name='Team',
        photo='AgACAgIAAxkBAAIQCWNoqnfQ4kvUznewXMC53GYygNSDAAI_vTEb5f9ISxxrGl7aDQXBAQADAgADeQADKwQ',
        invite_code='123'
    )

    await db.add_team_player(user_id=admin_id, team_id=team.id, is_captain=True)

    ids = [2, 3, 4]
    usernames = ['Sasha', 'Maxim', 'Alex']
    discords = ['Sasha#1234', 'Maxim#1234', 'Alex#1234']
    team_id = 1

    for index in range(len(usernames)):
        await db.add_user(user_id=ids[index], username=usernames[index])

    for index in range(len(usernames)):
        await db.add_member(
            user_id=ids[index],
            first_name=usernames[index],
            last_name=usernames[index],
            patronymic=usernames[index],
            group='Д192/2',
            member_type='STUDENT',
            institution='СПК'
        )

    for index in range(len(usernames)):
        await db.add_player(user_id=ids[index], discord=discords[index], fastcup=discords[index], username=usernames[index])

    for index in range(len(usernames)):
        await db.add_team_player(user_id=ids[index], team_id=team_id, is_participate=True)


async def telegram_bot():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config("bot.ini")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config
    sqlalchemy_database_uri = f'postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}'
    db_interaction = DBInteraction(sqlalchemy_url=sqlalchemy_database_uri, base=Base)
    db_interaction.create_tables()

    # await add_institutions(db=db_interaction)
    # await add_test_team(db=db_interaction, admin_id=config.tg_bot.admin_id)

    bot['db_model'] = db_interaction
    bot['kb'] = kb
    bot['phrases'] = Phrases

    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(telegram_bot())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
