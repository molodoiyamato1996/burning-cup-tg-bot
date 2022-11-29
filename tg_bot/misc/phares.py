class Phrases:
    start: str = 'Добро пожаловать'
    menu: str = '<b>💠 Главное меню</b>\n\n' \
                'Выберите действие:'

    you_need_to_register_to_continue: str = 'Чтобы продолжить вам надо пройти регистрацию'
    first_step_registration: str = '<b>#1 этап верификация\n\n</b>' \
                                   '<b>Кто вы?</b>'

    second_step_registration: str = '<b>#2 этап регистрации</b>\n\n' \
                                    '<b>Введите псевдоним:</b>\n\n' \
                                    '✅ Например: username'

    error_username_already_taken: str = '<b>❌ Псевдоним уже занят</b>'

    enter_fullname: str = '<b>Введите ФИО:</b>\n\n' \
                          '✅ Например: Иванов Иван Иванович'

    enter_fastcup: str = '<b>Введите Ваш fastcup:</b>\n\n' \
                         '✅ Например: username'
    error_fastcup_already_taken: str = '<b>❌ Fastcup уже занят</b>'

    enter_discrod: str = '<b>Введите Ваш discord:</b>\n\n' \
                         '✅ Например: username#1234'
    error_enter_correct_discrod: str = '<b>❌ Введите корректный дискорд!</b>\n\n' \
                                       '✅ Например: states#1234'
    error_discrod_already_taken: str = '<b>❌ Dicrod уже занят</b>'

    player_banned: str = '<b>🔒 Доступ запрещён</b>\n\n' \
                         'Вы были навсегда забанены на турнире\n\n' \
                         '<b>По причине:</b>\n'

    request_member_wait: str = '<b>⏳ Ваша заявка ожидает рассмотрения</b>\n\n' \
                               'Ожидайте уведомление 🛎'

    request_member_process: str = '<b>⏳ Ваша заявка проходит модерацию</b>\n\n' \
                                  'Ожидайте уведомление 🛎'

    request_member_success: str = ''

    request_member_fail: str = '<b>❌ Вы не прошли модерацию</b>\n\n' \
                               '<b>По причине:</b>\n'

    confirm_kick_team_player: str = 'Вы уверенны, что хотите кикнуть'
    success_kick_team_player: str = 'Игрок успешно кикнут!'

    confirm_disband_team: str = 'Вы уверенны, что хотите расформировать команду?'
    success_disband_team: str = 'Команда успешно распущена!'

    captain_verification_block: str = 'Во время верификации команды запрещено: менять название, изображение, кикать игроков и расформировывать команду!'
    team_player_verification_block: str = 'Во время верификации команды запрещено: менять псевдоним, дискорд, фасткап и покидать команду!'

    confirm_leave_from_team: str = 'Вы уверенны, что хотите покинуть команду?'
    success_leave_from_team: str = 'Вы успешно покинули команду!'

    enter_new_username: str = 'Введите новый псевдоним:'
    username_success_changed: str = '✅ Псевдоним успешно изменён'
    username_already_in_use: str = 'Данный псевдоним уже используется'

    enter_new_fastcup: str = 'Введите новый Фасткап:'
    fastcup_success_changed: str = '✅ Фасткап успешно изменён'
    fastcup_already_in_use: str = 'Данный Фасткап уже используется'

    enter_new_discord: str = 'Введите новый Дискорд:'
    discord_success_changed: str = '✅ Дискорд успешно изменён'
    discord_already_in_use: str = 'Данный Дискорд уже используется'

    day_title: str = '<b>День</b>\n\n'

    choice_action: str = 'Выберите действие:'

    confirm_finish_day: str = 'Вы уверенны, что хотите закончить день?'
    success_finish_day: str = 'День успешно завершён'

    tournament_title: str = '<b>Турнир</b>\n\n'

    teams_title: str = '<b>Команды</b>\n\n'
    players_title: str = '<b>Игроки</b>\n\n'
