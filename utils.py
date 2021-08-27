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
