import calendar
import time
from datetime import date, timedelta
from UserClass import User
from settings import weekdays_en
from utils import *
from DataBase import Schedule
from ParserDownload import download_schedules
from ParserTable import SchedulePars
import shutil
import os
from pathlib import Path


def user_schedule_on_day(telegram_id='', vk_id='', week=None, day=None, weekday=''):
    schedule = Schedule()
    if week is None:
        week = weeknum()
    if day is None:
        day = date.today()
    if schedule.select_user(telegram_id, vk_id) is None:
        raise KeyError("Пользователь не зарегистрирован")
    user = schedule.select_user(telegram_id=telegram_id, vk_id=vk_id)
    if weekday == '':
        day = calendar.day_name[day.weekday()]
    else:
        day = weekday
    select_res = schedule.select_day_by_user(day, user, week)
    res = f'{schedule.select_group_name(user.group_id)} {weekdays_en[day]} {week} неделя:\n'
    for subj in select_res:
        subj = list(subj)
        subj[0] = f'{subj[0]} {get_subj_time(int(subj[0]))}'
        subj.pop(1)
        new_subj = [str(el).replace('\n', ' ') if el != '' else '---' for el in subj]
        res += ' '.join(new_subj) + '\n'
    if len(select_res) == 0:
        res += 'Сегодня пар нет\n'
    if len(select_res) == 1 and 'Военная подготовка' in res:
        res = f'{schedule.select_group_name(user.group_id)} {weekdays_en[day]} {week} неделя:\n'
        res += 'Военная подготовка\n'
    schedule.con.close()
    return res


def user_schedule_on_exam(telegram_id='', vk_id='', week=None, day=None, weekday=''):
    schedule = Schedule()
    if week is None:
        week = weeknum()
    if day is None:
        day = date.today()
    if schedule.select_user(telegram_id, vk_id) is None:
        raise KeyError("Пользователь не зарегистрирован")
    user = schedule.select_user(telegram_id=telegram_id, vk_id=vk_id)
    if weekday == '':
        day = calendar.day_name[day.weekday()]
    else:
        day = weekday
    select_res = schedule.select_first_exams(day, user, week)
    res = f'{schedule.select_group_name(user.group_id)} {weekdays_en[day]} {week} неделя:\n'
    for subj in select_res:
        subj = list(subj)
        subj[0] = f'{subj[0]} {get_subj_time(int(subj[0]))}'
        subj.pop(1)
        new_subj = [str(el).replace('\n', ' ') if el != '' else '---' for el in subj]
        res += ' '.join(new_subj) + '\n'
    if len(select_res) == 0:
        res = ''
    schedule.con.close()
    return res

def user_schedule_on_week(telegram_id='', vk_id='', week=None):
    schedule = Schedule()
    if week is None:
        week = weeknum()
    if schedule.select_user(telegram_id, vk_id) is None:
        raise KeyError("Пользователь не зарегистрирован")
    days = list(calendar.day_name)[:-1]
    res = ''
    for day in days:
        res += user_schedule_on_day(telegram_id, vk_id, week, weekday=day) + '\n'
    schedule.con.close()
    return res

def user_schedule_on_exams(telegram_id='', vk_id='', week=None):
    schedule = Schedule()
    if week is None:
        week = weeknum()
    if schedule.select_user(telegram_id, vk_id) is None:
        raise KeyError("Пользователь не зарегистрирован")
    days = list(calendar.day_name)[:-1]
    res = ''
    for day in days:
        res += user_schedule_on_exam(telegram_id, vk_id, week, weekday=day) + '\n'
    schedule.con.close()
    return res

def today_schedule(telegram_id='', vk_id=''):
    return user_schedule_on_day(telegram_id, vk_id)


def nextday_schedule(telegram_id='', vk_id=''):
    week = weeknum()
    if calendar.day_name[date.today().weekday()] == 'Sunday':
        week += 1
    return user_schedule_on_day(telegram_id, vk_id, day=date.today() + timedelta(days=1), week=week)

def current_main_exams_schedule(telegram_id='', vk_id=''):
    schedule = Schedule()
    res = ""
    for exam in schedule.select_main_exams(schedule.select_user(telegram_id, vk_id)):
        res += ' '.join(list(map(str, exam)))
        res += '\n'
    schedule.con.close()
    return res

def current_week_schedule(telegram_id='', vk_id=''):
    return user_schedule_on_week(telegram_id, vk_id)

def current_first_exams_schedule(telegram_id='', vk_id=''):
    return user_schedule_on_exams(telegram_id, vk_id, 17) + user_schedule_on_exams(telegram_id, vk_id, 18)

def specify_week_schedule(telegram_id='', vk_id='', week=1):
    return user_schedule_on_week(telegram_id, vk_id, week)


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


def update_schedule():
    try:
        path = str(Path(__file__).parent.absolute())
        original = path + '/private/rasp.db'
        target = path + '/private/rasp1.db'
        shutil.copyfile(original, target)
        download_schedules()
        SchedulePars()
        SchedulePars(1)
        os.remove(original)
        os.rename(target, original)
        time.sleep(2)
    except Exception as e:
        print(e)
        return str(e)
    return 'Updated successfully'
