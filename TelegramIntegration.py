from telebot import TeleBot, types
from UserClass import User
from communication import insert_user, today_schedule, nextday_schedule, next_week_schedule, current_week_schedule, \
    get_current_weeknum, update_schedule, specify_week_schedule
from private.config import API_TOKEN

bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    bot.send_message(message.chat.id, 'Hello {}'.format(message.from_user.username))


@bot.message_handler(commands=['help'])
def send_help(message: types.Message):
    bot.send_message(message.chat.id,
                     'Напиши /today чтобы увидеть расписание на сегодня или /nextday - для завтрашнего дня. '
                     'Напиши /week чтобы увидеть расписание на текущую неделю или /nextweek для следующей. Чтобы '
                     'изменить текущую '
                     'группу введите ее название. '
                     'Чтобы узнать номер текущей недели введите /weeknumber')


@bot.message_handler(regexp=r"^(?ui)[а-я]{4}-\d{2}-\d{2}$")
def setup_user(message: types.Message):
    from_user = message.from_user
    user = User(from_user.first_name, from_user.last_name, from_user.id, group_name=message.text.upper())
    try:
        insert_user(user)
        bot.send_message(message.chat.id, f'Вы зарегистрированы как {message.text.upper()}')
    except IndexError as e:
        bot.send_message(message.chat.id, str(e))


@bot.message_handler(commands=['today'])
def today(message: types.Message):
    try:
        bot.send_message(message.chat.id, today_schedule(message.from_user.id))
    except KeyError as e:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы')


@bot.message_handler(commands=['nextday'])
def today(message: types.Message):
    try:
        bot.send_message(message.chat.id, nextday_schedule(message.from_user.id))
    except KeyError as e:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы')


@bot.message_handler(commands=['week'])
def current_week(message: types.Message):
    try:
        bot.send_message(message.chat.id, current_week_schedule(message.from_user.id))
    except KeyError as e:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы')


@bot.message_handler(commands=['nextweek'])
def next_week(message: types.Message):
    try:
        bot.send_message(message.chat.id, next_week_schedule(message.from_user.id))
    except KeyError as e:
        bot.send_message(message.chat.id, 'Вы не зарегистрированы')

@bot.message_handler(commands=['specialweek'])
def special_week(message: types.Message):
    try:
        week = int(message.text.split()[1])
        if 0 < week < 17:
            bot.send_message(message.chat.id, specify_week_schedule(message.from_user.id, week=week))
        else:
            bot.send_message(message.chat.id, f'{week} - недопустимый номер недели')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка. Вы ввели не число')
    except IndexError:
        bot.send_message(message.chat.id, 'Ошибка. Необходим аргумент - число')
    except Exception as e:
        bot.send_message(message.chat.id, str(e))


@bot.message_handler(commands=['weeknumber'])
def get_weeknum(message: types.Message):
    bot.send_message(message.chat.id, get_current_weeknum())


@bot.message_handler(commands=['update'])
def schedudle_update(message: types.Message):
    bot.send_message(message.chat.id, update_schedule())


@bot.message_handler()
def collect_trash(message: types.Message):
    bot.send_message(message.chat.id, 'Неверная команда. Введите /help чтобы увидеть список всех доступных команд')


def telegram_polling():
    bot.infinity_polling()
