import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tg_bot.keyboards import kb
from tg_bot.types.institution import InstitutionType
from tg_bot.types.moderator import ModeratorRule
from tg_bot.misc.phares import Phrases
from tg_bot.models.db_model.db_interaction import DBInteraction
from tg_bot.models.db_model import Base
from tg_bot.handlers import register_all_handlers

from tg_bot.types.team import TeamStatus


class TgBot:
    def __init__(self, config, schools: list, colleges: list, debug: bool = False):
        self.config = config
        self.debug = debug

        self.schools = schools
        self.colleges = colleges

        self.bot = Bot(token=self.config.tg_bot.token, parse_mode='HTML')

        self.sqlalchemy_database_uri = f'postgresql://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}'
        self.db_interaction = DBInteraction(sqlalchemy_url=self.sqlalchemy_database_uri, base=Base)
        self.db_interaction.create_tables()

        self.bot['config'] = self.config
        self.bot['kb'] = kb
        self.bot['phrases'] = Phrases
        self.bot['db_model'] = self.db_interaction

        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)

        logging.basicConfig(
            level=logging.INFO,
            format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        )
        self.logger = logging.getLogger(__name__)

    async def run(self, register_all_filters=None):
        self.logger.info("Starting bot")

        await self.add_admin_data()
        await self.add_institutions()

        if register_all_filters:
            register_all_filters(self.dp)

        register_all_handlers(self.dp)

        try:
            await self.dp.start_polling()
        finally:
            await self.dp.storage.close()
            await self.dp.storage.wait_closed()
            await self.bot.session.close()

    async def add_admin_data(self):
        admin_id = self.config.tg_bot.admin_id

        if not await self.db_interaction.is_user(user_id=admin_id):
            await self.db_interaction.add_user(user_id=admin_id, username='lxrd1995')

        if not await self.db_interaction.moderator_exist(user_id=admin_id):
            await self.db_interaction.add_moderator(user_id=admin_id, rule=ModeratorRule.ALL)

    async def add_institutions(self):
        for school in self.schools:
            if not await self.db_interaction.institution_exist(name=school):
                await self.db_interaction.add_institution(name=school, institution_type=InstitutionType.SCHOOL)

        for college in self.colleges:
            if not await self.db_interaction.institution_exist(name=college):
                await self.db_interaction.add_institution(name=college, institution_type=InstitutionType.COLLEGE)

    async def add_test_teams(self, count_teams: int):
        teams = []

        for i in range(0, count_teams, 0):
            pass

    async def add_test_tournament_teams(self, count_team: int):
        last_user_id = await self.db_interaction.get_last_user_id()
        discord = f'username#{last_user_id}'
        fastcup = f'username{last_user_id}'
        username = f'username{last_user_id}'

        count = count_team * 5

        for i in range(1, count + 1, 1):
            user_id = last_user_id + i
            username = username + i

            await self.db_interaction.add_user(user_id=user_id, username=username)
            await self.db_interaction.add_member(user_id=user_id, last_name='Иванов', first_name='Иван', patronymic='Иванович',
                                                 institution='СПК', member_type='STUDENT', group='Д192/2')
            await self.db_interaction.add_player(user_id=user_id, username=username, fastcup=fastcup, discord=discord, tg_username=username)

