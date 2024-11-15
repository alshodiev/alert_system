import pandas as pd
import seaborn as sns
import tia.bbg.datamgr as dm
import numpy as np
import sys
from datetime import datetime
import pymsteams
import time
import schedule
import matplotlib.pyplot as plt

es_initial = 0.6
ty_initial = 0.3
es_last = 0
ty_last = 0

def check_alert(es_initial = 0.6, ty_initial = 0.3, es_start = 0, ty_start = 0):
    global es_alrlevel, ty_alrtlevel, es_increment, ty_increment, es_last, ty_last

    webhook = None

    esalert= False
    tyalert = False
    esup = False
    tyup = False

    if es_start != 0:
        es_alrlevel = es_start

    if ty_start != 0:
        ty_alrlevel = ty_start

    es_increment = 0.6
    ty_increment = 0.3

    if datetime.now().hour == 17 and es_alrlevel != es_initial:
        es_alrlevel = es_initial
        es_last = 0
    if datetime.now().hour == 17 and ty_alrlevel != ty_initial:
        ty_alrlevel = ty_initial
        ty_last = 0
    
    mgr = dm.BbgDataManager()
    df = mgr.get_attributes(['ES1 Index', 'TY1 Comdty'], ['PX_LAST', 'CHG_NET_1D', 'CHG,PCT_1D'])

    if abs(df.loc['ES1 Index', 'CHG_PCT_1d'] - es_last) > es_alrlevel:
        if df.loc['ES1 Index', 'CHG_PCT_1d'] - es_last >0:
            esup = True
        else:
            esup = False

        es_alrt_text = # Some text that alerts the PX_LAST, CHG_NET_1D, Thresh of the alert level

        es_last = df.loc['ES1 Index', 'CHG_PCT_1d']
        es_alert = True
    # Same process for TY

    if esalert:
        if esup:
            myTeamsMessage = pymsteams.connectorcard(esuphook)
        else:
            myTeamsMessage = pymsteams.connectorcard(esdownhook)
        myTeamsMessage.text(es_alrt_text)
        myTeamsMessage.send()
    # Same process for tyalert

if datetime.now.weekday() == 5:
    exit()

schedule.clear()
check_alert(es_initial, ty_initial, es_initial, ty_initial)
schedule.every(3).minutes.do(check_alert)

while True and datetime.now().weekday() != 5:
    schedule.run_pending()
    time.sleep(1)

    if datetime.now().hour == 17:
        exit()
    if datetime.now().weekday() == 4: and datetime.now().hour > 17:
        exit()

