# VALR: Get Futures Contract Information


#%% Libraries
import pandas as pd
import numpy as np
import time
from datetime import datetime
from dateutil import parser
import json
import requests
import hashlib
import hmac
from configparser import ConfigParser
from valr_python import Client

#%% Config / Credentials
CONF_FILE = "config.cfg" # "algo_trading.cfg"

config = ConfigParser()
config.read(CONF_FILE)

API_KEY = config.get('valr_funding_arb', 'api_key')
API_SECRET = config.get('valr_funding_arb', 'api_secret')

#%% Parameters / Input Values / Constants
BASE_URL = "https://api.valr.com"
PAIR = "XRPUSDTPERP"

#%% Utilities
def sign_request(api_key_secret, timestamp, verb, path, body = ""):
    """Signs the request payload using the api key secret
    api_key_secret - the api key secret
    timestamp - the unix timestamp of this request e.g. int(time.time()*1000)
    verb - Http verb - GET, POST, PUT or DELETE
    path - path excluding host name, e.g. '/v1/withdraw
    body - http request body as a string, optional
    """
    payload = "{}{}{}{}".format(timestamp,verb.upper(),path,body)
    message = bytearray(payload,'utf-8')
    signature = hmac.new( bytearray(api_key_secret,'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
    return signature

def get_valr_headers(api_key, api_secret, path='/ws/account'):
    valr_headers = {}
    
    timestamp = int(time.time() * 1000)
    valr_headers["X-VALR-API-KEY"] = api_key
    valr_headers["X-VALR-SIGNATURE"] = sign_request(api_key_secret=API_SECRET, timestamp=timestamp,
                                                     verb='GET', path=path)
    valr_headers["X-VALR-TIMESTAMP"] = str(timestamp)  # str or byte req for request headers
    
    return valr_headers

def get_futures_info():
    
    path = "/v1/public/futures/info"
    url  = BASE_URL + path
    
    payload={}
    response = requests.request("GET", url, data=payload)
    
    response = json.loads(response.text) # parses a valid JSON string and converts it into a Python dictionary
    
    df = pd.DataFrame(response)
    
    print(df)

#%% Main
if __name__ == '__main__':
    get_futures_info()