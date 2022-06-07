"""
Data utility functions
"""
import os
import math
from urllib import error
from datetime import datetime, timedelta
import pandas as pd
from urllib3.exceptions import MaxRetryError, ConnectionError, ProtocolError
from ratelimit import limits, sleep_and_retry
from core.util import basic_io

# https://strftime.org/ python datetime formats
DAYS_IN_WEEK = 7
SATURDAY_INDEX = 5
SOCRATA_STR_DT_FORMAT = '%Y-%m-%d'

# data sourced from https://ibis.health.state.nm.us/resource/MMWRWeekCalendar.html#part3
# created from script sandbox/data/create_cdc_mmwr_lookup.py
CDC_RESOURCE_PATH = os.path.join("core", "resources", "cdc_week.json")
WEEK_END_TO_CDC_WEEK = basic_io.read_json_to_dict(CDC_RESOURCE_PATH)

# hard coded moving avg values
MOVING_AVG_WINDOW = 7
MOVING_AVG_COL_PREFIX = 'AVG7DAY_'

# time period for mapbox api
TIME_PERIOD = 60
API_LIMIT = 600

# location to zip path
LOC_ZIP_FILE_PATH = os.path.join("core", "resources", "location_zip.json")

# standarizing zipcode and date columns
STD_ZIP_COL_NAME = 'ZIPCODE'
STD_DATE_COL_NAME = 'STD_DATE'


def get_chicago_zipcodes():
    """
    read resource json to list of 59 chicago zipcodes

    :return: list of (str) where each str is zipcode of chicago
    """
    return basic_io.read_json_to_dict(os.path.join(
        "core", "resources", "chicago_zips_59.json"))


def get_zipcode_from_mapbox(lat, long, session, access_token):
    """
    get zipcode for geo coords.

    read in location to zip dict and attempt lookup
    if location is not in zip dict, call mapbox api
    add location, zip pair to dict then write to file

    :param lat: latitude
    :param long: longitude
    :param session: Session to make calls faster
    :param access_token: mapbox api access token
    :return: (str) zipcode for input long, lat
    """

    if math.isnan(lat) or math.isnan(long) or lat == 0.0 or long == 0.0:
        return None

    location = repr((long, lat))
    loc_to_zip_dic = basic_io.read_json_to_dict(LOC_ZIP_FILE_PATH)
    if location in loc_to_zip_dic:
        return loc_to_zip_dic[location]

    zipcode = get_zipcode_from_lat_long(lat, long, session, access_token)
    loc_to_zip_dic[location] = zipcode
    basic_io.write_dict_to_json(LOC_ZIP_FILE_PATH, loc_to_zip_dic)

    return zipcode


@sleep_and_retry
@limits(calls=API_LIMIT, period=TIME_PERIOD)
def get_zipcode_from_lat_long(lat, long, session, access_token):
    """
    get zipcode from mapbox api
    the api limits requests to 600 per min

    :param lat: latitude
    :param long: longitude
    :param session: Session to make calls faster
    :param access_token: mapbox api access token
    :return: zipcode
    """

    request_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{long},{lat}.json"
    params = {"types": "postcode", "access_token": access_token}

    try:
        response = session.get(url=request_url, params=params)
        zipcode = response.json()['features'][0]['text']
        return zipcode
    except error.HTTPError:
        print(request_url)
    except MaxRetryError:
        print(request_url)
    except ConnectionError:
        print(request_url)
    except ProtocolError:
        print(request_url)
    except IndexError:
        return None


def get_next_saturday(YYYY_MM_DD_str):
    """
    get date obj representing nearest saturday AFTER input date

    :param YYYY_MM_DD_str: (str) date in format 'YYYY-MM-DD'
    :return: datetime object representing the next saturday
    """
    date_obj = datetime.strptime(YYYY_MM_DD_str, SOCRATA_STR_DT_FORMAT)
    days_until_saturday = timedelta((SATURDAY_INDEX - date_obj.weekday()) % DAYS_IN_WEEK)
    return date_obj + days_until_saturday


def get_cdc_mmwr_week(YYY_MM_DD_str):
    """
    get CDC MMWR week for input date string (weeks are Sun-Sat)
    See https://ibis.health.state.nm.us/resource/MMWRWeekCalendar.html#part3

    :param YYY_MM_DD_str: (str) date
    :return: CDC week number
    """
    next_saturday = get_next_saturday(YYY_MM_DD_str)
    next_sat_str = next_saturday.strftime(SOCRATA_STR_DT_FORMAT)
    return WEEK_END_TO_CDC_WEEK[next_sat_str]


def compute_moving_avg_from_daily_data(daily_data_df, zipcode_col_name, date_col_name, cols_to_avg):
    """
    computes a 7 day average for input columns in cols_to_avg

    functions takes a pandas dataframe, the name of the column containing zipcode,
    the name of the column containing date, and a list of variables to be averaged.

    returns the dataframe with appended average columns
    (there will be one new column for every col in cols_to_avg, which
    represents the 7 day moving average for that col on that day)

    new columns names 'AVG7DAY_' + orig col name

    input:
        daily_data_df: pandas DataFrame
        zipcode_col_name (str) name of col containing zipcode
        date_col_name: (str) name of col containing date
        cols_to_avg: (list) of (str) where each item is name of col to be averaged

    returns:
        NA, appends cols to dataframe
    """

    daily_data_df.sort_values(date_col_name, inplace=True)

    for col_name in cols_to_avg:
        new_col_name = MOVING_AVG_COL_PREFIX + col_name
        daily_data_df[new_col_name] = (
            daily_data_df.groupby(zipcode_col_name)[col_name].
            rolling(window=MOVING_AVG_WINDOW).mean().reset_index(level=0, drop=True))


def convert_df_dtypes(data_df):
    """
    Updates the data types in data_df.
    If API returns data as str, use this function to convert numeric types.

        1. Attempts to convert all fields to numeric types (float or integer)
        2. Then converts non numeric types back to string

    input: pandas DataFrame
    returns: pandas DataFrame with modified dtypes

    """
    data_df = data_df.apply(pd.to_numeric, errors='ignore')
    data_df = data_df.convert_dtypes(convert_integer=False)
    return data_df


def is_valid_chicago_zip(zip_str):
    """
    returns true of string starts with '6'
    otherwise false

    input:
        zip_str: (str) zipcode string
    outout:
        boolean: true if valid chicago zip
    """
    if not zip_str or zip_str[0] != '6':
        return False

    return True


def standardize_zip_code_col(data_df, original_zip_col_name):
    """
    Standardize the zipcode column in a pandas DataFrame
    1. rename original_zip_col_name to STD_ZIP_COL_NAME (in place)
    2. convert col to string
    3. if not valid chicago zip (ie start with "6") replace with None

    :param data_df: pandas DataFrame containing zipcode col to standardize
    :param original_zip_col_name: (str) original zipcode col name
    :return: NA, modify df in place
    """
    data_df.rename(columns={original_zip_col_name: STD_ZIP_COL_NAME}, inplace=True)
    data_df[STD_ZIP_COL_NAME] = data_df[STD_ZIP_COL_NAME].astype(str)
    mask = data_df[STD_ZIP_COL_NAME].apply(is_valid_chicago_zip)
    data_df[STD_ZIP_COL_NAME][mask == False] = None # this throws a pandas SettingWithCopyWarning


def standardize_date_col(data_df, original_date_col_name):
    """
    Standardize the date column in a pandas DataFrame
    1. rename original_date_col_name to STD_DATE_COL_NAME (in place)
    2. standardize date format

    Output format is YYYY-MM-DD

    :param data_df: pandas DataFrame containing date col to standardize
    :param original_date_col_name: (str) original date col name
    :return: NA, modify df in place
    """
    data_df.rename(columns={original_date_col_name: STD_DATE_COL_NAME}, inplace=True)

    # this is pretty slow. not sure if necessary since a lot of them are already in this format
    # data_df[STD_DATE_COL_NAME] = \
    #     data_df[STD_DATE_COL_NAME].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d'))
    data_df[STD_DATE_COL_NAME] = pd.to_datetime(data_df[STD_DATE_COL_NAME],
                                                infer_datetime_format=True)
