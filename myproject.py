import requests
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
import random
import datetime, threading, time
import pathlib
from pathlib import Path
from keras.models import load_model
import pickle
import pandas as pd
import pretty_html_table
import os
from flask import Flask
from flask import render_template

file_name = Path(pathlib.Path.cwd(), 'parsing_folder', 'eco_sber_downloaded.csv')
collab_file_name = Path(pathlib.Path.cwd(), 'parsing_folder', 'collab_sber_downloaded.csv')

from parsing_folder.parsing_file import make_daily_download
from tokens_folder.get_tokens import get_eco_with_tokens
from tokens_folder.get_tokens import get_collab_with_tokens
from comments_kernel import get_comments_kernel

start_time = datetime.datetime.now()

def daily_download_call():
    global start_time
    delta = datetime.datetime.now()-start_time
    
    if delta.days >=1:
        
        start_time = datetime.datetime.now()
        make_daily_download(file_name, collab_file_name)
        get_eco_with_tokens(file_name)
        get_collab_with_tokens(collab_file_name)
        get_comments_kernel()
    
    
    threading.Timer(10000, daily_download_call ).start()
daily_download_call()

app = Flask(__name__)

@app.route('/')
def index():
    frontend_example = pd.read_pickle('kernel_file.pkl')
    frontend_example = pretty_html_table.build_table(frontend_example, 'blue_light', text_align='center', font_size='18px')
    return render_template('template.html', data=frontend_example)

if __name__ == '__main__':    
    app.run()







