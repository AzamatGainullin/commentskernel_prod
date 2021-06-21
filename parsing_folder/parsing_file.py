import requests
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
import random
import datetime, threading, time

### SMARTLAB FUNCTIONS ###

def smartlab_get_html(smartlab_last_page):
    r = requests.get(smartlab_last_page, headers=user_agent)
    return r.text

def smartlab_get_page_data(url, smartlab_writer):
    html = smartlab_get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    comments = soup.find_all('li', {'data-type': 'comment'})
    for comment in comments:
        name = comment.find('a', class_='a_name trader_other').text
        ct = comment.find('div', class_='text')
        if 'blockquote' in str(ct):
            try:
                ct.find("blockquote").extract()
            except:
                pass
        text = ct.text.strip()
        # print(text)
        date = comment.find('time')['datetime'][:10]
        data = {'name': name,
                    'text': text,
                    'date': date,
                    'url': url}
        smartlab_writer.writerow(data)

def smartlab_get_last_page_number():
    smartlab_last_page = 'https://smart-lab.ru/forum/SBER/page5883/'
    try:
        smartlab_html = smartlab_get_html(smartlab_last_page)
        smartlab_soup = BeautifulSoup(smartlab_html, 'lxml')
        smartlab_last_page_number = smartlab_soup.find('div', class_='pagination1').find_all('a')[-1]['href'][-5:-1]
        #print({'smartlab_last_page_number': smartlab_last_page_number})
        #smartlab_last_page_number = smartlab_soup.find('a', class_="page gradient last")['href'][-5:-1]
    except:
        print('SMARTLAB - CANT GET LAST PAGE NUMBER, SOME ERROR')
        raise TypeError
    return smartlab_last_page_number

smartlab_url = 'https://smart-lab.ru/forum/SBER/page{}/'



### MFD FUNCTIONS ###

user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
url = 'http://forum.mfd.ru/forum/thread/?id=62075&page={}'

def get_html(url):
    r = requests.get(url, headers=user_agent)
    return r.text

def get_last_page_number():
    last_page = 'http://forum.mfd.ru/forum/thread/?id=62075&page='
    try:
        html = get_html(last_page)
        soup = BeautifulSoup(html, 'lxml')
        paginator = soup.find('div', class_="mfd-paginator")
        last_page_number = paginator.find_all('a')[-1].text
    except:
        print('CANT GET LAST PAGE NUMBER, SOME ERROR')
        raise TypeError
    return last_page_number

def get_page_data(url, writer):
    try:
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        comments = soup.find_all('div', class_="mfd-post")
        for comment in comments:
            try:
                name = comment.find('div', class_='mfd-post-top-0').text
                ct = comment.find('div', class_='mfd-post-text')
                if 'blockquote' in str(ct):
                    try:
                        ct.find("blockquote").extract()
                    except:
                        pass
                text = ct.text.strip()
                date = comment.find('div', class_='mfd-post-top-1').text[:10]
                data = {'name': name,
                            'text': text,
                            'date': date,
                            'url': url}
                writer.writerow(data)
            except:
                #print(comment.text)
                pass
    except:
        sleep(10)
        print(url)
        pass

### COMMON FUNCTION ###
    
def make_daily_download(file_name, smartlab_file_name):
    last_page_number = get_last_page_number()
    with open(file_name, "r") as file:
        contents = file.readlines()
        str1 = contents[-1]
        #str1 = file.readline()
        downloaded_page_number = str1.split()[-1].split('=')[-1]
    if int(last_page_number)-2 > int(downloaded_page_number):
        with open(file_name, 'a') as f:
            order = ['name', 'text', 'date', 'url']
            writer = csv.DictWriter(f, fieldnames=order)
            for i in range(int(downloaded_page_number)+1, int(last_page_number)-1): # ЗДЕСЬ ПОМЕНЯЛ
                get_page_data(url.format(str(i)), writer)
                sleep(random.randrange(1,3))
        #print('MFD_TEST: work done, FILE CLOSED')

    smartlab_last_page_number = smartlab_get_last_page_number()
    with open(smartlab_file_name, "r") as file:
        scontents = file.readlines()
        sstr1 = scontents[-1]
        #str1 = file.readline()
        smartlab_downloaded_page_number = sstr1.split()[-1][-5:-1]
    if int(smartlab_last_page_number)-2 > int(smartlab_downloaded_page_number):
        with open(smartlab_file_name, 'a') as f:
            smartlab_order = ['name', 'text', 'date', 'url']
            smartlab_writer = csv.DictWriter(f, fieldnames=smartlab_order)
            for i in range(int(smartlab_downloaded_page_number)+1, int(smartlab_last_page_number)-1): # ЗДЕСЬ ПОМЕНЯЛ
                smartlab_get_page_data(smartlab_url.format(str(i)), smartlab_writer)
                sleep(random.randrange(1,3))
        #print('SMARTLAB_TEST: work done, FILE CLOSED')