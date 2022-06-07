import os
import requests
from core.util import basic_io

#######################################
###########   THE REQUEST   ###########
#######################################
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

resp = requests.get("https://data.cityofchicago.org/resource/naz8-j4nc.json?$select=cases_total, deaths_total", params={"$$app_token": keys[APP_TOKEN_STR]})


resp = requests.get("https://data.cityofchicago.org/resource/naz8-j4nc.json", params={"$$app_token": keys[APP_TOKEN_STR],
                                                                                                                        "$$select":['cases_total', 'deaths_total']})

