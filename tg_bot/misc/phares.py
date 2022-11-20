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
