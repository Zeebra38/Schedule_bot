from aiogram import Bot, Dispatcher, executor, types

from UserClass import User
from communication import insert_user, today_schedule, nextday_schedule, next_week_schedule, current_week_schedule, \
    get_current_weeknum
from private.config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Hello {}'.format(message.from_user.username))


@dp.message_handler(regexp=r"^(?ui)[а-я]{4}-\d{2}-\d{2}$")
async def setup_user(message: types.Message):
    from_user = message.from_user
    user = User(from_user.first_name, from_user.last_name, from_user.id, group_name=message.text.upper())
    try:
        insert_user(user)
        await message.answer(f'Вы зарегистрированы как {message.text.upper()}')
    except IndexError as e:
        await message.answer(str(e))


@dp.message_handler(commands=['today'])
async def today(message: types.Message):
    await message.answer(today_schedule(message.from_user.id))


@dp.message_handler(commands=['nextday'])
async def today(message: types.Message):
    await message.answer(nextday_schedule(message.from_user.id))


@dp.message_handler(commands=['week'])
async def current_week(message: types.Message):
    await message.answer(current_week_schedule(message.from_user.id))


@dp.message_handler(commands=['nextweek'])
async def next_week(message: types.Message):
    await message.answer(next_week_schedule(message.from_user.id))


@dp.message_handler(commands=['weeknumber'])
async def get_weeknum(message: types.Message):
    await message.answer(get_current_weeknum())


@dp.message_handler()
async def collect_trash(message: types.Message):
    await message.reply('Неверная команда. Введите /help чтобы увидеть список всех доступных команд')


def telegram_polling():
    executor.start_polling(dp, skip_updates=True)


telegram_polling()
