"""
Functions for retrieving demographic data from census api
"""
import requests
import pandas as pd
from core.util import api_util
from core.data import data_transformations

# there is census data for all 59 of the zipcodes in chicago_zips_59.json
# EXCEPT for 60666

# ACS API Documentation:
# https://www.census.gov/content/dam/Census/library/publications/2020/acs/acs_api_handbook_2020.pdf

# We're using the 2019 ACS 5-year data profiles
# Full list of variables: https://api.census.gov/data/2019/acs/acs5/profile/variables.html

ZIP_COL_NAME = data_transformations.STD_ZIP_COL_NAME
zip_lst = data_transformations.get_chicago_zipcodes()
ZIPS = ",".join(zip_lst)
CENSUS_API_KEY = api_util.get_census_key()

var_to_colname_dict = {'NAME': 'zcta', 'DP02_0016E': 'hhold_size',
                 'DP02_0017E': 'fam_size',
                 'DP03_0005PE': 'unemploy_rate',
                 'DP03_0062E': 'median_income',
                 'DP03_0119PE': 'pct_below_poverty_lvl',
                 'DP05_0018E': 'median_age',
                 'DP05_0024PE': 'pct_65_or_older',
                 'DP05_0071PE': 'pct_hispanic',
                 'DP05_0080PE': 'pct_asian',
                 'DP05_0078PE': 'pct_black',
                 'DP05_0077PE': 'pct_white',
                 'DP05_0081PE': 'pct_pacific_islander',
                 'DP05_0079PE': 'pct_american_indian',
                 'DP05_0082PE': 'pct_other_race',
                 'DP02_0062PE': 'pct_high_school_grad',
                 'DP02_0152PE': 'pct_hholds_w_computer',
                 'DP02_0153PE': 'pct_hholds_w_internet',
                 'DP03_0096PE': 'pct_w_health_insur'
                 }

var_to_desc_dict = {'NAME': 'Zip Code Tabluation Area', 'DP02_0016E': 'Average hhold size',
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

VARIABLE_LST = ",".join(var_to_colname_dict.keys())
var_to_colname_dict['zip code tabulation area'] = ZIP_COL_NAME

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

    data_df = data_transformations.convert_df_dtypes(data_df)

    # rename columns
    data_df = data_df.rename(columns=var_to_colname_dict)

    return data_df
