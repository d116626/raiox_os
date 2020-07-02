#!/usr/bin/python3
import pandas as pd
import numpy as np
import pandas_gbq
import pydata_google_auth
import gspread
from gcloud import storage
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import os
from os import listdir
import requests
import json
from datetime import datetime
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot, offline
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')

import manipulation


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../../credentials/gabinete_sv_credentials.json"





def read_sheets(sheet_name, workSheet=0):


    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('../../credentials/gabinete-sv-9aed310629e5.json', scope)
    gc          = gspread.authorize(credentials)
    if workSheet==0:
        wks         = gc.open(sheet_name).sheet1
    else:
        wks = gc.open(sheet_name).worksheet(workSheet)
        
    data        = wks.get_all_values()
    headers     = data.pop(0)

    return pd.DataFrame(data, columns=headers)



