from collections import defaultdict
import requests
import api_rte as RTE
import pandas as pd
import datetime

########  ODRE #########

GLOBAL_TEMPO = {}

def getTempoFromAPI(date):

    if date not in GLOBAL_TEMPO:
        GLOBAL_TEMPO[date] = {}

        date_from = pd.to_datetime(date)
        date_from = date_from + pd.DateOffset(days=-1)
        date_from=date_from.replace(hour = 0, minute = 0)
        date_to = date_from + pd.DateOffset(months=3)
        date_to=date_to.replace(hour = 23, minute = 45)

        if date_to > datetime.datetime.now():
            date_to = datetime.datetime.now()

        r_tempo = RTE.get_tempo(date_from, date_to)

        for iteratedDate in r_tempo["tempo_like_calendars"]["values"]:
            curDate=iteratedDate["start_date"] #2023-08-04T15:34:00+02:00 (Format classique)
            curDate= datetime.datetime.fromisoformat(curDate)
            date = curDate.strftime("%Y-%m-%d") #2014-11-25 (on rattrape sur le format géré précédemment par le script)
            GLOBAL_TEMPO[date] = iteratedDate["value"]
    return GLOBAL_TEMPO[date]

class TempoCalGetter:
    def __init__(self):
        return

    def get(self, jour):
        value = getTempoFromAPI(jour) 
        return getTempoFromAPI(jour)