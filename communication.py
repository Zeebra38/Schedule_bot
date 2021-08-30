# todo Функции, которые будут возвращать готовый к отправке пользователю string
import calendar
from datetime import date

from settings import schedule, weekdays_en
from utils import *


def user_schedule_on_day(telegram_id='', vk_id='', week=weeknum(), day=date.today(), weekday=''):
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
    return res


def user_schedule_on_week(telegram_id='', vk_id='', week=weeknum()):
    days = list(calendar.day_name)[:-1]
    res = ''
    for day in days:
        res += user_schedule_on_day(telegram_id, vk_id, week, weekday=day) + '\n'
    return res
