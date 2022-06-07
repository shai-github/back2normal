import requests
import pandas as pd
from core.util import api_util
from core.data import data_transformations

# ACS API Documentation:
# https://www.census.gov/content/dam/Census/library/publications/2020/acs/acs_api_handbook_2020.pdf
# VARIABLE_LST

# We're using the 2019 ACS 5-year data profiles
# Full list of variables: https://api.census.gov/data/2019/acs/acs5/profile/variables.html

zip_lst = data_transformations.get_chicago_zipcodes()
ZIPS = ",".join(zip_lst)
CENSUS_API_KEY = api_util.get_census_key()

variable_dict = {'NAME': 'Zipcode', 'DP02_0016E': 'Average hhold size',
                 'DP02_0017E': 'Average family size',
                 'DP03_0005PE': 'Unemployment rate for pop. >= 16 years in labor force',
                 'DP03_0062E': 'Median household income (dollars)',
                 'DP03_0119PE': 'Pct. of pop. w/ income below poverty level in last 12 months',
                 'DP05_0018E': 'Median age (years)',
                 'DP05_0024PE': 'Pct of pop. 65 years or older',
                 'DP05_0071PE': 'Pct. of pop. that is Hispanic or Latino (of any race)',
                 'DP05_0080PE': 'Pct of pop. that is Asian (and not Hispanic)',
                 'DP05_0078PE': 'Pct of pop. that is Black or African American (and not Hispanic)',
                 'DP05_0077PE': 'Pct of pop. that is White (and not Hispanic)',
                 'DP05_0081PE': 'Pct of pop. that is Native Hawaiian and Other Pacific Islander (and not Hispanic)',
                 'DP05_0079PE': 'Pct of pop. that is American Indian and Alaska Native (and not Hispanic)',
                 'DP05_0082PE': 'Pct of pop. that is some other race (and not Hispanic)',
                 'DP02_0062PE': 'Pct. of pop. (>= 25 years) w/ high school degree',
                 'DP02_0152PE': 'Pct. of hholds w/ a computer',
                 'DP02_0153PE': 'Pct. of hholds w/ broadband internet',
                 'DP03_0096PE': 'Pct. of pop. w/ health insurance coverage',
                 }
VARIABLE_LST = ",".join(variable_dict.keys())

query_url = (f"https://api.census.gov/data/2019/acs/acs5/profile?"
             f"get={VARIABLE_LST}&for=zip%20code%20tabulation%20area:{ZIPS}"
             f"&in=state:17&key={CENSUS_API_KEY}")


def get_census_data_from_api():
    """
    downloads pre-selected census demographic data by zip code from census API

    returns pandas DataFrame with one row per zip code

    """
    resp = requests.get(query_url)
    data_lsts = resp.json()
    headers = data_lsts.pop(0)
    data_df = pd.DataFrame(data_lsts, columns=headers)

    #convert dtypes should be moved into a function
    data_df = data_df.apply(pd.to_numeric, errors='ignore')
    data_df = data_df.convert_dtypes(convert_integer=False)
    
    #zip codes should be strings
    data_df['zip code tabulation area'] = data_df['zip code tabulation area'].astype(str)

    #rename columns
    data_df = data_df.rename(columns=variable_dict)

    return data_df
