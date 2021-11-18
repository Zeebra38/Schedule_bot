import os
from TelegramIntegration import telegram_polling
from threading import Thread
from Vkontakte import vk_polling
from asyncio import new_event_loop, set_event_loop
from yadupload import download_from_disk


def main_task():
    if os.path.exists('private/rasp.db'):
        os.remove('private/rasp.db')
    download_from_disk()
    vk = Thread(target=vk_polling)
    vk.start()
    tg = Thread(target=telegram_polling())
    tg.start()


if __name__ == '__main__':
    set_event_loop(new_event_loop())
    main_task()
