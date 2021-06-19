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

file_name = Path(pathlib.Path.cwd(), 'parsing_folder', 'mfd_sber_downloaded.csv')
smartlab_file_name = Path(pathlib.Path.cwd(), 'parsing_folder', 'smartlab_sber_downloaded.csv')
print('DOWNLOAD AGAIN AND AGAIN...')

from parsing_folder.parsing_file import make_daily_download
from tokens_folder.get_tokens import get_mfd_with_tokens
from tokens_folder.get_tokens import get_smartlab_with_tokens
from comments_kernel import get_comments_kernel

#frontend_example = 0

import datetime
 
start_time = datetime.datetime.now()

def daily_download_call():
    global start_time
    delta = datetime.datetime.now()-start_time
    print('HERE WE GO... DAYLI CALL AGAIN')
    if delta.days >=1:
        print('DELTA DAYS > = 1')
        start_time = datetime.datetime.now()
        make_daily_download(file_name, smartlab_file_name)
        get_mfd_with_tokens(file_name)
        get_smartlab_with_tokens(smartlab_file_name)
        get_comments_kernel()
    
    
    threading.Timer(600, daily_download_call ).start()
daily_download_call()






frontend_example = pd.read_pickle('kernel_file.pkl')







import pandas as pd
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return frontend_example.to_html()

if __name__ == '__main__':    
    app.run()






