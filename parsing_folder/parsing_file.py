import requests
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
import random
import datetime, threading, time
import pandas as pd
import pathlib
from pathlib import Path

df_env = pd.read_csv(Path(pathlib.Path.cwd(), 'dicer'))

collab_last_page = df_env.collab_last_page.iloc[0]
collab_url = df_env.collab_url.iloc[0]
url = df_env.url.iloc[0]
last_page = df_env.last_page.iloc[0]

### colLAB FUNCTIONS ###

def collab_get_html(collab_last_page):
    r = requests.get(collab_last_page, headers=user_agent)
    return r.text

def collab_get_page_data(url, collab_writer):
    html = collab_get_html(url)
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
        collab_writer.writerow(data)

def collab_get_last_page_number():
    
    try:
        collab_html = collab_get_html(collab_last_page)
        collab_soup = BeautifulSoup(collab_html, 'lxml')
        collab_last_page_number = collab_soup.find('div', class_='pagination1').find_all('a')[-1]['href'][-5:-1]
        #print({'collab_last_page_number': collab_last_page_number})
        #collab_last_page_number = collab_soup.find('a', class_="page gradient last")['href'][-5:-1]
    except:
        print('colLAB - CANT GET LAST PAGE NUMBER, SOME ERROR')
        raise TypeError
    return collab_last_page_number





### eco FUNCTIONS ###

user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


def get_html(url):
    r = requests.get(url, headers=user_agent)
    return r.text

def get_last_page_number():
    
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
    
def make_daily_download(file_name, collab_file_name):
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
            for i in range(int(downloaded_page_number)+1, int(last_page_number)-1):
                get_page_data(url.format(str(i)), writer)
                sleep(random.randrange(1,3))
        #print('eco_TEST: work done, FILE CLOSED')

    collab_last_page_number = collab_get_last_page_number()
    with open(collab_file_name, "r") as file:
        scontents = file.readlines()
        sstr1 = scontents[-1]
        #str1 = file.readline()
        collab_downloaded_page_number = sstr1.split()[-1][-5:-1]
    if int(collab_last_page_number)-2 > int(collab_downloaded_page_number):
        with open(collab_file_name, 'a') as f:
            collab_order = ['name', 'text', 'date', 'url']
            collab_writer = csv.DictWriter(f, fieldnames=collab_order)
            for i in range(int(collab_downloaded_page_number)+1, int(collab_last_page_number)-1): # ЗДЕСЬ ПОМЕНЯЛ
                collab_get_page_data(collab_url.format(str(i)), collab_writer)
                sleep(random.randrange(1,3))
        #print('colLAB_TEST: work done, FILE CLOSED')