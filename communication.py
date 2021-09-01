# todo Функции, которые будут возвращать готовый к отправке пользователю string
import calendar
from datetime import date, timedelta
from DataBase import Schedule
from UserClass import User
from settings import weekdays_en
from utils import *


def user_schedule_on_day(telegram_id='', vk_id='', week=weeknum(), day=date.today(), weekday=''):
    schedule = Schedule()
    if schedule.select_user(telegram_id, vk_id) is None:
        raise KeyError("Пользователь не зарегистрирован")
    user = schedule.select_user(telegram_id=telegram_id, vk_id=vk_id)
    if weekday == '':
        day = calendar.day_name[day.weekday()]
    else:
        day = weekday
    select_res = schedule.select_day_by_user(day, user, week)
    res = f'Группа - {schedule.select_group_name(user.group_id)} {weekdays_en[day]} {week} неделя:\n'
    for subj in select_res:
        subj = list(subj)
        subj[0] = f'{subj[0]} {get_subj_time(int(subj[0]))}'
        subj.pop(1)
        new_subj = [str(el).replace('\n', ' ') if el != '' else '---' for el in subj]
        res += ' '.join(new_subj) + '\n'
    if len(select_res) == 0:
        res += 'Сегодня пар нет\n'
    schedule.con.close()
    return res


def user_schedule_on_week(telegram_id='', vk_id='', week=weeknum()):
    schedule = Schedule()
    if schedule.select_user(telegram_id, vk_id) is None:
        raise KeyError("Пользователь не зарегистрирован")
    days = list(calendar.day_name)[:-1]
    res = ''
    for day in days:
        res += user_schedule_on_day(telegram_id, vk_id, week, weekday=day) + '\n'
    schedule.con.close()
    return res


def today_schedule(telegram_id='', vk_id=''):
    return user_schedule_on_day(telegram_id, vk_id)


def nextday_schedule(telegram_id='', vk_id=''):
    return user_schedule_on_day(telegram_id, vk_id, day=date.today() + timedelta(days=1))


def current_week_schedule(telegram_id='', vk_id=''):
    return user_schedule_on_week(telegram_id, vk_id)


def next_week_schedule(telegram_id='', vk_id=''):
    return user_schedule_on_week(telegram_id, vk_id, weeknum() + 1)


def get_current_weeknum():
    return f'Текущая неделя - {weeknum()}'


def insert_user(user: User):
    schedule = Schedule()
    if schedule.check_group(user.group_name) is not None:
        exists = schedule.select_user(user.telegram_id, user.vk_id) is not None
        if not exists:
            schedule.insert_user(user)
        else:
            schedule.update_user(user)
        schedule.con.close()
    else:
        schedule.con.close()
        raise IndexError("Ошибка. Такой группы нет в базе")
