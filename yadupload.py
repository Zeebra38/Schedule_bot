import os
import time
import yadisk
from private.config import tokenya
import datetime
from math import fabs

y = yadisk.YaDisk(token=tokenya)
time0 = datetime.datetime.now()


def upload_to_disk(force=False):
    now = datetime.datetime.now()
    global time0
    delta = now - time0
    delta_sec = delta.total_seconds()
    delta_hours = divmod(delta_sec, 3600)[0]
    if fabs(delta_hours) > 1 or force:
        time0 = datetime.datetime.now()
        try:
            if y.exists('/Data/Schedule_bot/rasp.db'):
                y.remove('/Data/Schedule_bot/rasp.db')
            time.sleep(2)
            try:
                y.upload('private/rasp.db', '/Data/Schedule_bot/rasp.db')
            except Exception as e:
                pass
            print(f'uploaded at {datetime.datetime.now()}')
        except Exception as e:
            print(e)


def download_from_disk():
    if os.path.exists('private/rasp.db'):
        os.remove('private/rasp.db')
    y.download('/Data/Schedule_bot/rasp.db', 'private/rasp.db')

