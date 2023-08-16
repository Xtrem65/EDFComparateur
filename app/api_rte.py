import urllib
import requests
import pandas as pd

from api_config import *
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
    #df = json_to_pd_tempo(r_json)

    return r_json


def get_prod(start_date, end_date, production_type=None, type=None,
             oauth_url=OAUTH_URL,
             client_id=EDF_CLIENT_ID,
             client_secret=EDF_CLIENT_SECRET,
             url_prod=URL_PROD):
    """ General method to download RTE forecasts production

    :param start_date:
    :param end_date:
    :param production_type:
    :param type:
    :param oauth_url:
    :param client_id:
    :param client_secret:
    :param url_prod:
    :return:
    """
    token_type, access_token = get_token(oauth_url=oauth_url, client_id=client_id,
                                         client_secret=client_secret)
    res_json = get_production_json(start_date, end_date, token_type, access_token,
                                   production_type=production_type, type=type, url_prod=url_prod)

    res = parse_production(res_json)
    return res


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


def _parse_json_values(values):
    """ Convert RTE data data from dictionnry form to pandas DataFrame.

    :param values:
    :return: pandas.DataFrame
    """
    df = pd.DataFrame.from_dict(values)
    df.index = df.start_date
    df.start_date = pd.to_datetime(df.start_date, format='%Y-%m-%d %H:%M:%S', utc=True)
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S', utc=True)
    df.updated_date = pd.to_datetime(df.updated_date, format='%Y-%m-%d %H:%M:%S', utc=True)
    df.end_date = pd.to_datetime(df.end_date, format='%Y-%m-%d %H:%M:%S', utc=True)
    df.sort_index(inplace=True)

    return df


def json_to_pd_tempo(r_tempo):
    """ Convert Tempo RTE data from json to pandas data frame

    :param r_tempo:
    :return: pandas.DataFrame
    """
    values_dict = r_tempo.get('tempo_like_calendars').get('values')
    df = _parse_json_values(values_dict)
    return df