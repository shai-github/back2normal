import os
import requests
from core.util import basic_io

# in .config/ create socrata_chicago_keys.json with contents:
'''
{"api_key":"<your-api-key>",
 "api_secret_key":"<your-secret-key>",
 "app_token":"<your-app-token>"}
 '''

API_KEY_STR = "api_key"
API_SECRET_KEY_STR = "api_secret_key"
APP_TOKEN_STR = "app_token"

path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
keys = basic_io.read_json_to_dict(path_to_keys)

resp = requests.get("https://data.cityofchicago.org/resource/naz8-j4nc.json", params={"$$app_token": keys[APP_TOKEN_STR]})

## socrata api v2 provides headers that include field name and type
## not sure if this is exposed via sodapy
## could try to programmatically write create table statement from these
## but the dtype is not specific, ie number and not float, int, etc
resp.headers['X-SODA2-Fields']
resp.headers['X-SODA2-Types']
