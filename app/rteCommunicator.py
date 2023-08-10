import api_rte as RTE
import datetime

class RteCommunicator:

    def __init__(self) -> None:
        self.token = RTE.get_token()
        self.tempoCalendar = {}
        
    def getTempo(self, expectedStartDate=datetime.datetime(2022,1,1,0,0), expectedEndDate=datetime.datetime.today()):

        tempoCalendar = {}

        start_date = expectedStartDate
        iterated_end_date   = start_date + datetime.timedelta(days=300)
        i = 0

        while iterated_end_date <= expectedEndDate:
            # Requetes aux service tempo et prod + traitement
            r_tempo = RTE.get_tempo(start_date, iterated_end_date)
            start_date = iterated_end_date + datetime.timedelta(days=1)
            iterated_end_date += datetime.timedelta(days=300)
            
            for iteratedDate in r_tempo["tempo_like_calendars"]["values"]:
                curDate=iteratedDate["start_date"] #2023-08-04T15:34:00+02:00 (Format classique)
                curDate= datetime.datetime.fromisoformat(curDate)
                date = curDate.strftime("%Y-%m-%d") #2014-11-25 (on rattrape sur le format géré précédemment par le script)
                tempoCalendar[date] = iteratedDate["value"]
        
        #On a fini les iterations massive, reste juste à faire un dernier jet
        iterated_end_date    = expectedEndDate + datetime.timedelta(days=1)
        start_date = start_date + datetime.timedelta(days=-1)
        r_tempo     = RTE.get_tempo(start_date, iterated_end_date)

        for iteratedDate in r_tempo["tempo_like_calendars"]["values"]:
            curDate=iteratedDate["start_date"] #2023-08-04T15:34:00+02:00 (Format classique)
            curDate= datetime.datetime.fromisoformat(curDate)
            date = curDate.strftime("%Y-%m-%d") #2014-11-25 (on rattrape sur le format géré précédemment par le script)
            tempoCalendar[date] = iteratedDate["value"]
        return tempoCalendar

rte = RteCommunicator()
rte.getTempo()

