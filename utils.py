from datetime import datetime




def translate_weekday(weekday: str):
    from settings import weekdays_ru
    weekday = weekday.lower().capitalize()
    return weekdays_ru[weekday]


def weeknum():
    zero = datetime(2021, 9, 1)
    now = datetime.today()
    # now = datetime(2021, 2, 8) #расскоментить для изменения даты
    delta = now - zero
    deltaweeks = 1
    # print(delta.days)
    if delta.days >= 7:
        buf = delta.days
        while buf >= 7:
            deltaweeks += 1
            buf = buf - 7
    return deltaweeks


def get_subj_time(number: int):
    if number == 1:
        return '09:00-10:30'
    if number == 2:
        return '10:40-12:10'
    if number == 3:
        return '12:40-14:10'
    if number == 4:
        return '14:20-15:50'
    if number == 5:
        return '16:20-17:50'
    if number == 6:
        return '18:00-19:30'
