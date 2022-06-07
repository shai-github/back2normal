import os
import requests
import sqlite3
import pandas as pd
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

resp = requests.get("https://data.cityofchicago.org/resource/naz8-j4nc.json", params={"$$app_token": keys[APP_TOKEN_STR]})

# field name and general data type
resp.headers['X-SODA2-Fields']
resp.headers['X-SODA2-Types']

# to pandas df
df = pd.DataFrame.from_dict(resp.json())

#######################################
###########   Creat table   ###########
#######################################

# create db and insert data
conn = sqlite3.connect('testdb.db')
df.to_sql('my_table', conn, if_exists='replace')

# it's reading everything in as string except for first field
cursor = conn.cursor()
print(cursor.execute("pragma table_info('my_table')").fetchall())
print(cursor.execute("select * from my_table").fetchall())

pd.set_option('display.max_columns', None)
print(df.head())
print(df.dtypes)

#######################################
########### Attempts to Fix ###########
#######################################

# infer type via convert_dtypes
# either converts all to strings or does nothing
df_infer_dtype = df.convert_dtypes(convert_string=False)
print(df_infer_dtype.dtypes)

########### Use pd.to_numeric, then infer type with convert_dtype
# errors=ignore seems scary?
df_numeric = df.apply(pd.to_numeric, errors='ignore')
print(df_numeric.dtypes)
print(df_numeric.head())

# converts the date var to string and leaves int and floats
df_numeric_and_strings = df_numeric.convert_dtypes(convert_integer=False)
print(df_numeric_and_strings.dtypes)
print(df_numeric_and_strings.head())

df_numeric_and_strings.to_sql('my_better_table', conn, if_exists='replace')
print(cursor.execute("pragma table_info('my_better_table')").fetchall())
