import asyncio
import datetime
import logging

from tg_bot import TgBot, register_all_handlers, register_all_filters, kb, Base, DBInteraction
from tg_bot.config import load_config
from data import schools, colleges


async def add_admin_data(db, admin_id: int):
    user = await db.add_user(user_id=admin_id, username='skywalker')
    await db.add_moderator(user_id=admin_id, rule='ALL')
    await db.add_member(
        user_id=admin_id,
        last_name='Иванов',
        first_name='Иван',
        patronymic='Иванович',
        institution='СПК',
        group='Д192/2',
        member_type='STUDENT'
    )
    await db.add_player(user_id=admin_id, username='skywalker', discord='skywalker#1234', fastcup='skywalker')


async def add_tournament_teams(db):
    for index in range(1, 17, 1):
        team_name = f'team{index}'
        players = []

        for i in range(1, 6, 1):
            user_id = index * 5 + i + i * 8
            print(user_id)
            username = f'username{user_id}'
            discord = f'{username}#1234'

            await db.add_user(user_id=user_id, username=username)

            await db.add_member(
                user_id=user_id,
                last_name='test',
                first_name='test',
                patronymic='test',
                institution='СПК',
                group='Д192/2',
                member_type='STUDENT',
            )

            player = await db.add_player(
                user_id=user_id,
                username=username,
                discord=discord,
                fastcup=username
            )

            if i == 5:
                captain = player
            else:
                players.append(player)

        await db.add_tournament_team(
            captain_id=captain.id,
            players=players,
            name=team_name,
            photo=f'{team_name}.png'
        )


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

config = load_config('bot.ini')
tg_bot = TgBot(config=config, schools=schools, colleges=colleges)

if __name__ == '__main__':
    try:
        asyncio.run(tg_bot.run(register_all_filters=register_all_filters, register_all_handlers=register_all_handlers))
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
