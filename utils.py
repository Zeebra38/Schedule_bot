from datetime import datetime
def translate_weekday(weekday: str):
    weekday = weekday.lower().capitalize()
    if weekday == 'Понедельник':
        return 'Monday'
    if weekday == 'Вторник':
        return 'Tuesday'
    if weekday == 'Среда':
        return 'Wednesday'
    if weekday == 'Четверг':
        return 'Thursday'
    if weekday == 'Пятница':
        return 'Friday'
    if weekday == 'Суббота':
        return 'Saturday'

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