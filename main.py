from TelegramIntegration import telegram_polling
from threading import Thread
from Vkontakte import vk_polling
from asyncio import new_event_loop, set_event_loop

def main_task():
    vk = Thread(target=vk_polling)
    vk.start()
    tg = Thread(target=telegram_polling())
    tg.start()



if __name__ == '__main__':
    set_event_loop(new_event_loop())
    main_task()