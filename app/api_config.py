"""
Ici, on configure toutes les clefs de config de l'APP pour ce connecter aux API externes

Actuellement, le code est connecté à :

- L'API RTE pour synchroniser les types de jour Tempo (Bleu/Blanc/Rouge)
- L'API ODRE pour synchroniser le gCO2/kwH et les moyens de production d'énergie FR dans le passé

Concernant l'API RTE : 
Etape 1 - Pour demander/retrouver un client ID/Secret : https://data.rte-france.com/group/guest/apps
Etape 2 - Souscrire à https://data.rte-france.com/catalog/-/api/consumption/Tempo-Like-Supply-Contract/v1.1

Merci à https://github.com/ReinboldV/api_rte 
pour l'exemple d'utilisation de cette api

Concernant l'API ODRE
Etape 1 - Pour obtenir une clé API  : https://odre.opendatasoft.com/account/api-keys/

Merci à https://github.com/sourceperl/sandbox/blob/1c2182573beefa658859a61ba3b254abe24c5b4f/open_data/rte_live.py#L11
pour l'exemple d'utilisation de cette api


Merci à github pour la fonction de recherche globale dans le code de tout l'univers
"""
import os

###########
#  TEMPO  #
###########

# Pensez à souscrire à https://data.rte-france.com/catalog/-/api/consumption/Tempo-Like-Supply-Contract/v1.1

# Client ID and secret code, you can get those at https://data.rte-france.com/
EDF_CLIENT_ID = os.environ["EDF_CLIENT_ID"]
EDF_CLIENT_SECRET = os.environ["EDF_CLIENT_SECRET"]

###### RTE TEMPO
# URL for authentication and get a token access :
OAUTH_URL = 'https://digital.iservices.rte-france.com/token/oauth/'

# list of available API :
URL_TEMPO = 'https://digital.iservices.rte-france.com/open_api/tempo_like_supply_contract/v1/tempo_like_calendars'
URL_PROD  = 'https://digital.iservices.rte-france.com/open_api/generation_forecast/v2/forecasts'
URL_CONSO = 'https://digital.iservices.rte-france.com/open_api/consumption/v1'

###########
#  ODRE   #
###########

ODRE_APIKEY = os.environ["ODRE_APIKEY"]