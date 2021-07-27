import bs4
import re
import requests
import functools
from bs4 import BeautifulSoup
import os, shutil, threading


def download(link: str, barrier):
    (dirname, filename) = os.path.split(link)
    # pattern = r'(заоч)|!|(МИРЭА)'
    # result = re.match(pattern, filename)
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
    all_a = []
    links = []
    all_a = soup.find('ul', class_="uk-switcher uk-margin").find('li').find_all('a')
    links = []
    for a in all_a:
        if 'webservices' in a['href'] and '.xlsx' in a['href'] and 'КБиСП' in a['href']: #убрать потом КБиСП
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
