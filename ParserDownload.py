import os
import shutil
import threading
import pyexcel as p
import requests
from bs4 import BeautifulSoup


def download(link: str, barrier):
    (dirname, filename) = os.path.split(link)
    result = 'заоч' in filename or 'МИРЭА' in filename or '!' in filename
    if result:
        pass
    else:
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            with open('schedules/' + filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    barrier.wait()


def find_links():
    rez = requests.get('https://www.mirea.ru/schedule/')
    soup = BeautifulSoup(rez.content, 'lxml')
    all_a = soup.find('ul', class_="uk-switcher uk-margin").find('li').find_all('a')
    links = []
    for a in all_a:
        if 'webservices' in a['href'] and '.xlsx' in a['href'] and (
                'КБиСП' in a['href'] or 'Киб' in a['href'] or 'ИИТ' in a['href']):  # убрать потом конкретные институты
            links.append(a['href'])
    return links


def download_schedules():
    if os.path.exists('schedules'):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'schedules')
        shutil.rmtree(path)
    os.mkdir('schedules')
    links = find_links()
    barrier = threading.Barrier(len(links) + 1)
    for link in links:
        threading.Thread(target=download, args=[link, barrier]).start()
    barrier.wait()
    for file_name in os.listdir('schedules/'):
        if '.xlsx' not in file_name:
            p.save_book_as(file_name=file_name, dest_file_name='schedules/' + file_name[:-4] + '.xlsx')