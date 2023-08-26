from collections import defaultdict
import api_rte as RTE
import pandas as pd
import datetime
from api_config import *
import redis

r = redis.Redis(host=REDIS_ADDRESS, port=6379, db=0)

########  ODRE #########
def getTempoFromAPI(date):

    redisKey = 'TEMPO-'+date
    currentMemoryTempoValue = r.get(redisKey)
    if currentMemoryTempoValue == None :
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
            iteratingRedisKey = 'TEMPO-'+date
            r.set(iteratingRedisKey,iteratedDate["value"])
    return r.get(redisKey).decode('UTF-8')

class TempoCalGetter:
    def __init__(self):
        return

    def get(self, jour):
        return getTempoFromAPI(jour)