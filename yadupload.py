import os
import time
import yadisk
from private.config import tokenya
import datetime
from math import fabs
import pytz

y = yadisk.YaDisk(token=tokenya)
my_tz = pytz.timezone("Europe/Moscow")
time0 = datetime.datetime.now(my_tz)


def upload_to_disk(force=False):
    now = datetime.datetime.now(my_tz)
    global time0
    delta = now - time0
    delta_sec = delta.total_seconds()
    delta_hours = divmod(delta_sec, 3600)[0]
    if fabs(delta_hours) > 0 or force:
        time0 = datetime.datetime.now(my_tz)
        try:
            if y.exists('/Data/Schedule_bot/rasp.db'):
                y.remove('/Data/Schedule_bot/rasp.db')
            time.sleep(2)
            try:
                y.upload('private/rasp.db', '/Data/Schedule_bot/rasp.db')
            except Exception as e:
                pass
            print(f'uploaded at {datetime.datetime.now(my_tz)}')
        except Exception as e:
            print(e)


def download_from_disk():
    if os.path.exists('private/rasp.db'):
        os.remove('private/rasp.db')
    y.download('/Data/Schedule_bot/rasp.db', 'private/rasp.db')
