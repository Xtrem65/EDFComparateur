import urllib
import requests

from api_config import *

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

