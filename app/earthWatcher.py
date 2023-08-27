from collections import defaultdict
import requests
import pandas as pd
from datetime import date as DATE
import traceback
########  ODRE #########
"""

Details des champs, un peu reorganisés à partir d'un exemple
"fields": {
"consommation": 36414,
"taux_co2": 55,

"nucleaire": 29374,

"eolien_terrestre": "ND",
"eolien": 1707,
"eolien_offshore": "ND",

"hydraulique": 4652,
"hydraulique_lacs": 579,
"hydraulique_fil_eau_eclusee": 3820
"hydraulique_step_turbinage": 253,
"pompage": -1631,

"gaz": 3599,
"gaz_tac": 0,
"gaz_autres": 0,
"gaz_ccg": 3179,
"gaz_cogen": 422,

"fioul": 143,
"fioul_cogen": 29,
"fioul_tac": 1,
"fioul_autres": 113,

"charbon": 6,

"ech_physiques": -2435,

"bioenergies": 999,
"bioenergies_dechets": 168,
"bioenergies_biomasse": 560,
"bioenergies_biogaz": 276,

"solaire": 0,
"stockage_batterie": "ND",
"destockage_batterie": "ND",

"heure": "04:15",
"nature": "Données temps réel",
"date_heure": "2022-06-01T02:15:00+00:00",
"date": "2022-06-01",
"prevision_j1": 36150,
"prevision_j": 36400,
"perimetre": "France",
},
"""
GLOBAL_PRODUCTION_DATA_DETAILS = {}

def getProductionDetails(date):

    if date not in GLOBAL_PRODUCTION_DATA_DETAILS:
        GLOBAL_PRODUCTION_DATA_DETAILS[date] = {}

        date_from = pd.to_datetime(date)
        date_from = date_from + pd.DateOffset(days=-1)
        date_from=date_from.replace(hour = 0, minute = 0)
        date_to = date_from + pd.DateOffset(months=3)

        if date_to.date() > DATE.today():
            date_to = date_to.replace(day=DATE.today().day-1,month=DATE.today().month,year=DATE.today().year)

        date_to=date_to.replace(hour = 23, minute = 45)

        paramsReadyDateFrom = date_from.strftime("%Y-%m-%dT%H:%M:%S")
        paramsReadyDateTo = date_to.strftime("%Y-%m-%dT%H:%M:%S")
        print("Retrieving Eco2Mix details  ("+ paramsReadyDateFrom+" to "+paramsReadyDateTo+")")
        params = {
            'dataset':'eco2mix-national-tr',
            #'refine.date_heure': date, #Fonctionne pour query un seul jour
            'q':'date_heure>=%s AND date_heure <= %s'%(paramsReadyDateFrom, paramsReadyDateTo),
            'rows':9600, #100 jours
            'sort':'-date',
            'facet':'date_heure'
        }

        details = requests.get('https://opendata.reseaux-energies.fr/api/records/1.0/search/', params=params).json()
        dataset= details["records"]

        for horodateDataSet in dataset:
            cleanedData = {}
            #On s'en tape des autres données
            horodateDataSet = horodateDataSet["fields"]

            if horodateDataSet["date"] not in GLOBAL_PRODUCTION_DATA_DETAILS:
                GLOBAL_PRODUCTION_DATA_DETAILS[horodateDataSet["date"]] = {}

            cleanedData["gCO2/kWh"] = horodateDataSet["taux_co2"]
            conso = horodateDataSet["consommation"]
            cleanedData["conso"] = conso

            nukePercent = (horodateDataSet["nucleaire"] / conso)
            cleanedData["nukePercent"] = nukePercent
            
            # On récupère le volume eolien
            #On ignore horodateDataSet["eolien_terrestre"] + horodateDataSet["eolien_offshore"]
            totalEolien = horodateDataSet["eolien"] 
            eolienPercent = (totalEolien / conso)
            cleanedData["eolienPercent"] = eolienPercent

            # On récupère le volume PV
            # On considère le stockage/destockage batterie comme de l'eolien
            totalSolaire = horodateDataSet["solaire"] #+ horodateDataSet["stockage_batterie"] + horodateDataSet["destockage_batterie"]
            solairePercent = (totalSolaire / conso)
            cleanedData["solairePercent"] = solairePercent


            # On récupère le volume hydro
            totalHydro = horodateDataSet["hydraulique"] + horodateDataSet["pompage"]
            hydrauPercent = (totalHydro / conso)
            cleanedData["hydrauPercent"] = hydrauPercent

            # On récupère le volume biomasse
            totalBioEnergies = horodateDataSet["bioenergies"]
            bioenergiesPercent = (totalBioEnergies / conso)
            cleanedData["bioenergiesPercent"] = bioenergiesPercent

            # On récupère le volume fossile
            totalFossile = horodateDataSet["charbon"] + horodateDataSet["fioul"] + horodateDataSet["gaz"]
            fossilePercent = (totalFossile / conso)
            cleanedData["fossilePercent"] = fossilePercent

            # On récupère le volume d'échanges
            totalEchanges = horodateDataSet["ech_physiques"]
            echangesPercent = (totalEchanges / conso)
            cleanedData["echangesPercent"] = echangesPercent

            #checkSommePourcent = nukePercent+eolienPercent+hydrauPercent+solairePercent+bioenergiesPercent+fossilePercent+echangesPercent
            GLOBAL_PRODUCTION_DATA_DETAILS[horodateDataSet["date"]][horodateDataSet["heure"]] = cleanedData
    return GLOBAL_PRODUCTION_DATA_DETAILS[date]

class EarthWatcher:
    def getEmptyConsoDict(self):
        return {
            "Nucleaire" : 0,
            "Hydraulique" : 0,
            "Eolienne": 0,
            "Solaire" : 0,
            "BioEnergies" : 0,
            "Fossiles" : 0,
            "Echanges" : 0,
            }
    
    def __init__(self):
        self.totalConso = 0
        self.totalCO2 = 0


        self.prefillDataSince2022()
        self.totalDetailedConso = self.getEmptyConsoDict()
        self.monthlyDetailedConso = {
            "Nucleaire" : {},
            "Hydraulique" : {},
            "Eolienne": {},
            "Solaire" : {},
            "BioEnergies" : {},
            "Fossiles" : {},
            "Echanges" : {},
            }

        #Si on trouve pas de données de prod pour un créneau, on utilise le dernier créneau fonctionnel, et on mémorise le volume incertain ici
        self.totalConsoEnIncertitude=0
        self.lastWorkingProductionDetails = {}

    def prefillDataSince2022(self):
        print("2022-1")
        getProductionDetails("2022-07-02")
        print("2022-2")
        getProductionDetails("2022-04-02")
        print("2022-3")
        getProductionDetails("2022-04-02")
        print("2022-3")
        getProductionDetails("2022-07-02")
        print("2022-4")
        getProductionDetails("2022-10-02")
        print("2023-1")
        getProductionDetails("2023-01-02")
        print("2023-2")
        getProductionDetails("2023-04-02")
        print("2023-3")
        getProductionDetails("2023-07-02")
        print("2023 over")
        #Ca fait des trucs chelous ici

    def getTotalDetailedConso(self):
        return self.totalDetailedConso
    def getMonthlyDetailedConso(self):
        return self.monthlyDetailedConso
    def getFiabilité(self):
        return "%.2f%%" % ((self.totalConsoEnIncertitude/self.totalConso)*100)
    def getTotalConso(self):
        return round(self.totalConso,2)
    def getCO2(self):
        return round(self.totalCO2/1000,2)
    
    def getValueByOrigin(self):
        return {
            "Nucleaire" : self.totalConsoNuke,
            "Hydraulique" : self.totalConsoHydrau,
            "Eolienne": self.totalConsoEolienne,
            "Solaire" : self.totalConsoSolaire,
            "BioEnergies" : self.totalConsoBioEnergies,
            "Fossiles" : self.totalConsoFossiles,
            "Echanges" : self.totalConsoEchanges,
        }
    def getColorList(self):
        return {
            "Nucleaire" : "#58d0e8",
            "Hydraulique" : "#112599",
            "Eolienne": "#99004C",
            "Solaire" : "#FFCC00",
            "BioEnergies" : "#009900",
            "Fossiles" : "#000000",
            "Echanges" : "#606060"
        }
    def getColorByOrigin(self, source):
        return self.getColorList()[source]
        
    def addConsoToCounters(self, conso, jour):
        currentMonth = jour[:-3]
        for key, value in self.monthlyDetailedConso.items():
            if currentMonth not in self.monthlyDetailedConso[key]: 
                self.monthlyDetailedConso[key][currentMonth] = 0

        for key in conso.keys():
            self.totalDetailedConso[key] += conso[key]
            self.monthlyDetailedConso[key][currentMonth] += conso[key]

    def addConsummatedHour(self, conso, heure, jour):
        heure=heure[:-3]

        self.totalConso = self.totalConso + conso
        try:
            prodDuJour = getProductionDetails(jour)
            heureEnCours = prodDuJour[heure]
        except BaseException as e:
            self.totalConsoEnIncertitude = self.totalConsoEnIncertitude + conso
            heureEnCours = self.lastWorkingProductionDetails
            traceback.print_exc()

        self.totalCO2 = self.totalCO2 + (heureEnCours["gCO2/kWh"])* conso
        currentConso = {
            "Nucleaire" : conso * heureEnCours["nukePercent"],
            "Hydraulique" : conso * heureEnCours["hydrauPercent"],
            "Eolienne": conso * heureEnCours["eolienPercent"],
            "Solaire" : conso * heureEnCours["solairePercent"],
            "BioEnergies" : conso * heureEnCours["bioenergiesPercent"],
            "Fossiles" : conso * heureEnCours["fossilePercent"],
            "Echanges" : conso * heureEnCours["echangesPercent"],
        }
        self.addConsoToCounters(currentConso, jour)

        #On memorise ces données de prod pour les reutiliser s'il nous manque des infos sur le prochain créneau
        self.lastWorkingProductionDetails = heureEnCours

