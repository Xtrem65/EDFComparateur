"""
Script for configuring RTE API access.

This script is user dependant, Please change client ID and client secret code before using it.
working directory are also case dependant.
Merci https://github.com/ReinboldV/api_rte
"""

# Client ID and secret code, you can get those at https://data.rte-france.com/
CLIENT_ID       = ''
CLIENT_SECRET   = '980620be-b568-4971-aebb-cb316b7dd991'

# URL for authentication and get a token access :
OAUTH_URL = 'https://digital.iservices.rte-france.com/token/oauth/'

# list of available API :
URL_TEMPO = 'https://digital.iservices.rte-france.com/open_api/tempo_like_supply_contract/v1/tempo_like_calendars'
URL_PROD  = 'https://digital.iservices.rte-france.com/open_api/generation_forecast/v2/forecasts'
URL_CONSO = 'https://digital.iservices.rte-france.com/open_api/consumption/v1'

# list of available production types
PRODUCTION_TYPE = ['WIND', 'SOLAR', 'AGGREGATED_CPC', 'AGGREGATED_PROGRAMMABLE_FRANCE', 'AGGREGATED_NON_PROGRAMMABLE_FRANCE', 'AGGREGATED_FRANCE', 'MDSE' , 'MDSETRF', 'MDSESTS']

# list of available production forecasts types
TYPE = ['D-3', # 3 days ahead
        'D-2', # 2 days ahead
        'D-1', # 1 days ahead
        'CURRENT', # current
        'ID'] # intra-day