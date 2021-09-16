from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from private.config import vk_session
from vk_api.utils import get_random_id
from communication import insert_user, today_schedule, nextday_schedule, next_week_schedule, current_week_schedule, \
    get_current_weeknum, specify_week_schedule
from UserClass import User

vk = vk_session.get_api()

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Сегодня')

keyboard_ls = VkKeyboard(one_time=False)
keyboard_ls.add_button('Расписание ')

keyboard_infinity = VkKeyboard(one_time=True)
keyboard_infinity.add_button('Расписание на сегодня', color=VkKeyboardColor.POSITIVE)
keyboard_infinity.add_button('На завтра', color=VkKeyboardColor.POSITIVE)
keyboard_infinity.add_line()
keyboard_infinity.add_button('Расписание на неделю', color=VkKeyboardColor.POSITIVE)
keyboard_infinity.add_button('На следующую неделю', color=VkKeyboardColor.POSITIVE)
keyboard_infinity.add_line()
keyboard_infinity.add_button('Выход', color=VkKeyboardColor.PRIMARY)

keyboard_admin = VkKeyboard(one_time=True)
keyboard_admin.add_button('update', color=VkKeyboardColor.POSITIVE)


def send(id, text, peremennaya, ls: int, msg_id=0):
    """ls == 1 - личка. Else - группа"""

    if ls == 1:
        vk.messages.send(
            keyboard=keyboard_infinity.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),
            message=text,
            user_id=id
        )
    elif ls == 2:  # Скидывает в личку пустое пересланное ПОЛНОСТЬЮ сообщение
        vk.messages.send(
            # keyboard=keyboard_ls.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),

            forward_messages=msg_id,
            user_id=id
        )
    elif ls == 3:
        vk.messages.send(
            keyboard=keyboard_infinity.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),
            message=text,
            user_id=id
        )
    elif peremennaya == 1:
        vk.messages.send(
            keyboard=keyboard.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),
            message=text,
            chat_id=id
        )
    # vk_session.method('messages.send',
    #                {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard.get_keyboard()})
    elif peremennaya == 2:
        vk.messages.send(
            keyboard=keyboard_admin.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),
            message=text,
            chat_id=id
        )

        """vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, #отправление сообщений в лс
                                        'keyboard': keyboard_admin.get_keyboard()})  # отправление сообщений"""
    elif peremennaya == 3:
        vk.messages.send(
            keyboard=keyboard_infinity.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),
            message=text,
            chat_id=id
        )
        """vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0,
                                        'keyboard': keyboard_infinity.get_keyboard()})  # отправление сообщений с бесконечной клавой"""
    elif peremennaya == 4:
        vk.messages.send(
            keyboard=keyboard_ls.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),
            message=text,
            chat_id=id
        )
        """vk_session.method('messages.send',
                          {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard_ls.get_keyboard()})"""
    elif peremennaya == 6:  # Скидывает в группу пустое пересланное ПОЛНОСТЬЮ сообщение
        vk.messages.send(
            # keyboard=keyboard_ls.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),

            forward_messages=msg_id,
            chat_id=id
        )
    else:
        vk.messages.send(
            # keyboard=keyboard_ls.get_keyboard(),
            key=('576ad401c5edfcfac1bfe9f3c88b277add2c8dfc'),
            server=('https://lp.vk.com/wh186219261'),
            ts=('2325'),
            random_id=get_random_id(),
            message=text,
            chat_id=id
        )


def vk_raspisanie(id: int, msg: str, ls: int):

    if '-' in msg[4:5] and '-' in msg[7:8] and len(msg) == 10: #Регистрация группы todo first name last name
        user = User(' ', ' ', vk_id=id, group_name = msg.upper())
        try:
            insert_user(user)
            send(id, 'Вы зарегистрированы как {}'.format(msg), 0, ls)
        except IndexError as e:
            send(id, str(e), 0, ls)



    if "неделя" in msg:

        try:
            week = int(msg.split()[1])
            if 0 < week < 17:
                send(id, specify_week_schedule(vk_id = id, week = week), 0, ls)
            else:
                send(id, f'{week} - недопустимый номер недели', 0, ls)
        except ValueError:
            send(id, 'Ошибка. Вы ввели не число', 0, ls)

        except IndexError:
            send(id, 'Ошибка. Необходим аргумент - число', 0, ls)

        except Exception as e:
            send(id, str(e), 0, ls)

    if "номер недели" in msg:

        try:

            send(id, get_current_weeknum(), 0, ls)
        except IndexError as e:
            send(id, str(e), 0, ls)


    if 'расписание на сегодня' in msg:

        try:
            send(id, today_schedule(vk_id=id), 0, ls)
        except KeyError:
            send(id, 'Ошибка. Возможно вы не зарегестрированы', 0, ls)
    if 'на завтра' in msg:
        try:
            send(id, nextday_schedule(vk_id=id), 0, ls)
        except KeyError:
            send(id, 'Ошибка. Возможно вы не зарегестрированы', 0, ls)

    if 'расписание на неделю' in msg:
        try:
            send(id, current_week_schedule(vk_id=id), 0, ls)
        except KeyError:
            send(id, 'Ошибка. Возможно вы не зарегестрированы', 0, ls)
    if 'на следующую' in msg:
        try:
            send(id, next_week_schedule(vk_id= id), 0, ls)
        except KeyError:
            send(id, 'Ошибка. Возможно вы не зарегестрированы', 0, ls)
    if '[club186219261|@public186219261] расписание' == msg or 'расписание' == msg:
        if ls == 1:
            send(id, 'Для изменения группы напишите ее название', 0, ls)
        send(id, 'Выберите вид расписания ', 3, ls)

    if '[club186219261|@public186219261] выход' == msg:
        send(id, 'Выхожу :C', 0, ls)


    if 'update' in msg:
        pass
        #download()
        #update(main_class)
        #send(id, 'Расписание обновлено!', 0, ls)




# def update_ED(main_class): todo метод
#     try:
#         while True:
#             if getday_week_time_etc()[1] == 1:
#                 download()
#                 update(main_class)
#                 send(68659003, 'Расписание обновлено', 2, 1)
#                 send(152014637, 'Расписание обновлено', 2, 1)
#                 time.sleep(7200)
#             else:
#                 time.sleep(7200)
#     except Exception as rrr:
#         with open('update.txt', 'a', encoding='utf-8') as f:
#             f.write(f'{rrr} update down\n')
