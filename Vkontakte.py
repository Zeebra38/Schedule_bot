import os
import threading
import time as t1
from datetime import datetime, time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from VKUtils import vk_raspisanie, send
from private.config import vk_session

def thread_gr():
    try:
        longpoll = VkBotLongPoll(vk_session, 186219261)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:  # проверка нового сообщения
                msg = event.message.text.lower()
                if event.from_chat:  # сообщение в группу  # содержание сообщения
                    id = event.chat_id  # IDшник чата
                    vk_raspisanie(id, msg, 0)
                    msg_id = event.message.conversation_message_id

    except Exception as rrr:
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} {rrr} group continue \n')
        try:
            send(68659003, f'{datetime.now()}  \n  {rrr} group', 2, 1)          #ЛС Мише Р.
            send(152014637, f'{datetime.now()}  \n  {rrr} group continue', 2, 1)#ЛС Илье Д.
            t1.sleep(1800)
        except Exception as err:
            with open('logs1.txt', 'a', encoding='utf-8') as f:
                f.write(f'{datetime.now()} {rrr} group continue \n')
            t1.sleep(1800)
        threading.Thread(target=thread_gr).start()


def thread_ls():
    try:
        lslongpoll = VkLongPoll(vk_session)
        for event in lslongpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:  # проверка нового сообщения
                msg = event.text.lower()
                msg_id = event.message_id
                if event.to_me:  # сообщение в лс сообщества
                    if event.from_user:
                        idid = event.user_id
                        vk_raspisanie(idid, msg, 1)


    except Exception as rrr:
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} {rrr} ls pass\n')
        try:
            send(68659003, f'{datetime.now()}  \n  {rrr} ls', 2, 1)
            send(152014637, f'{datetime.now()}  \n  {rrr} ls pass', 2, 1)
            t1.sleep(1800)
        except Exception as rrr:
            with open('logs1.txt', 'a', encoding='utf-8') as f:
                f.write(f'{datetime.now()} {rrr} ls pass\n')
            t1.sleep(1800)
        threading.Thread(target=thread_ls).start()
        # x.start()


def vk_polling():
    x1 = threading.Thread(target=thread_ls)
    x2 = threading.Thread(target=thread_gr)
    x1.start()
    x2.start()

""" 
1. Сделать вывод расписания на сегодня - завтра
2. Прописать все функции if '' in msg
. ЛС
. Полезные штуки: или удобные
кнопка с инфой важное
обращение от лица старосты и/или пересылание по id
ящерка
"""
