import urllib
import requests

from api_config import *

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
    if date in GLOBAL_PRODUCTION_DATA_DETAILS:
        print ("Found Data for"+ date)
    else: 
        GLOBAL_PRODUCTION_DATA_DETAILS[date] = {}
        details = requests.get('https://opendata.reseaux-energies.fr/api/records/1.0/search/'
            '?dataset=eco2mix-national-tr&rows=96&sort=-date'
            '&facet=date_heure&refine.date_heure=%s' % date).json()
        dataset= details["records"]
        for horodateDataSet in dataset:
            cleanedData = {}
            #On s'en tape des autres données
            horodateDataSet = horodateDataSet["fields"]
            print("Looking at new dataset")
            print(horodateDataSet["date"])
            print(horodateDataSet["heure"])
            cleanedData["CO2"] = horodateDataSet["taux_co2"]
            conso = horodateDataSet["consommation"]
            cleanedData["conso"] = conso

            nukePercent = (horodateDataSet["nucleaire"] / conso) * 100
            cleanedData["nukePercent"] = nukePercent
            
            # On récupère le volume eolien
            #On ignore horodateDataSet["eolien_terrestre"] + horodateDataSet["eolien_offshore"]
            totalEolien = horodateDataSet["eolien"] 
            eolienPercent = (totalEolien / conso) * 100
            cleanedData["eolienPercent"] = eolienPercent

            # On récupère le volume PV
            # On considère le stockage/destockage batterie comme de l'eolien
            totalSolaire = horodateDataSet["solaire"] #+ horodateDataSet["stockage_batterie"] + horodateDataSet["destockage_batterie"]
            solairePercent = (totalSolaire / conso) * 100
            cleanedData["solairePercent"] = solairePercent


            # On récupère le volume hydro
            totalHydro = horodateDataSet["hydraulique"] + horodateDataSet["pompage"]
            hydrauPercent = (totalHydro / conso) * 100
            cleanedData["hydrauPercent"] = hydrauPercent

            # On récupère le volume biomasse
            totalBioEnergies = horodateDataSet["bioenergies"]
            bioenergiesPercent = (totalBioEnergies / conso) * 100
            cleanedData["bioenergiesPercent"] = bioenergiesPercent

            # On récupère le volume fossile
            totalFossile = horodateDataSet["charbon"] + horodateDataSet["fioul"] + horodateDataSet["gaz"]
            fossilePercent = (totalFossile / conso) * 100
            cleanedData["fossilePercent"] = fossilePercent

            # On récupère le volume d'échanges
            totalEchanges = horodateDataSet["ech_physiques"]
            echangesPercent = (totalEchanges / conso) * 100
            cleanedData["echangesPercent"] = echangesPercent

            checkSommePourcent = nukePercent+eolienPercent+hydrauPercent+solairePercent+bioenergiesPercent+fossilePercent+echangesPercent
            print("Total : %f " % checkSommePourcent)
            print("Now remembering CleanedData")
            print(cleanedData)
            
            GLOBAL_PRODUCTION_DATA_DETAILS[date][horodateDataSet["heure"]] = cleanedData

    return GLOBAL_PRODUCTION_DATA_DETAILS[date]

######## RTE / TEMPO #########

# Merci https://github.com/ReinboldV/api_rte
def get_token(oauth_url=OAUTH_URL, client_id=EDF_CLIENT_ID, client_secret=EDF_CLIENT_SECRET):
    """

    :param oauth_url:
    :param client_id:
    :param client_secret:
    :return: [token_type, access_token]
    """

    r = requests.post(oauth_url, auth=(client_id, client_secret))
    if r.ok:
        access_token = r.json()['access_token']
        token_type = r.json()['token_type']
    else:
        Warning("Authentication failed")
        access_token = None
        token_type = None

    return token_type, access_token


def get_tempo(start_date, end_date,
              oauth_url=OAUTH_URL,
              client_id=EDF_CLIENT_ID,
              client_secret=EDF_CLIENT_SECRET,
              url_tempo=URL_TEMPO):
    """

    :param client_secret:
    :param client_id:
    :param oauth_url:
    :param start_date:
    :param end_date:
    :param url_tempo:
    :return:
    """

    token_type, access_token = get_token(oauth_url=oauth_url, client_id=client_id, client_secret=client_secret)
    r_json = get_tempo_json(start_date, end_date, token_type, access_token, url_tempo=url_tempo)
    return r_json


def get_tempo_json(start_date, end_date, token_type, access_token, url_tempo=URL_TEMPO):
    """

    :param access_token:
    :param start_date:
    :param end_date:
    :param token_type:
    :param url_tempo:
    :return:
    """

    start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')
    end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S+02:00')

    param = {'start_date': start_str, 'end_date': end_str}
    url_tempo = url_tempo
    url_tempo += '?' + urllib.parse.urlencode(param).replace("%3A", ":")

    r = requests.get(url_tempo, headers={'Authorization': f'{token_type} {access_token}'}, params=param)

    return r.json()

