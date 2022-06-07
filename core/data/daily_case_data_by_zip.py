"""
Functions for retrieving daily covid case data from
https://il-covid-zip-data.s3.us-east-2.amazonaws.com/latest/zips.csv
Data is returned as csv
"""
import os
import csv
import requests
import pandas as pd
from core.data import data_transformations

# citation:
# https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv

CSV_URL = 'https://il-covid-zip-data.s3.us-east-2.amazonaws.com/latest/zips.csv'
CSV_FILE_PATH = os.path.join("core", "resources", "IDPH", "idph_covid_daily.csv")

SQL_TABLE_NM = 'DAILY_COVID_CASE_DATA'

# hardcoded data fields
DATE_COL_NAME = 'date'
ZIP_COL_NAME = 'zipcode'
CASES_COL = 'confirmed_cases'
CASES_CHANGE_COL = 'confirmed_cases_change'
TESTED_COL = 'total_tested'
TESTED_CHANGE_COL = 'total_tested_change'

SELECT_COLUMNS = [DATE_COL_NAME, ZIP_COL_NAME,
                  CASES_COL, CASES_CHANGE_COL,
                  TESTED_COL, TESTED_CHANGE_COL]

COLS_TO_AVG = [CASES_COL, CASES_CHANGE_COL, TESTED_COL]


def get_daily_covid_data_from_api(testing=False):
    """
    downloads historical IDPH daily covid case data by zipcode
    if testing is true, read data from csv instead

    returns pandas DataFrame with columns in SELECT_COLUMNS

    """

    if testing:
        return get_daily_covid_data_from_file()

    with requests.Session() as s:
        download = s.get(CSV_URL)

        # returns the entire csv as string
        decoded_content = download.content.decode('utf-8')

        # readout is a _csv.reader object
        readout = csv.reader(decoded_content.splitlines(), delimiter=',')

        # list of list, where each list is a row and 0th row is header
        data_list = list(readout)
        data_df = pd.DataFrame(data_list[1:], columns=data_list[0])

        # select columns to keep
        select_df = data_df.loc[:, SELECT_COLUMNS]
        return select_df


@DeprecationWarning
def compute_7_day_mavg_columns_for_IDPH_data(daily_data_df):
    """
    Computes weekly average columns listed in COLS_TO_AVG
    Appends columsn to daily_data_df

    :param daily_data_df: daily covid data DataFrame
    :return: NA modifies input DataFrame in place
    """

    data_transformations.compute_moving_avg_from_daily_data(daily_data_df,
                                                            ZIP_COL_NAME,
                                                            DATE_COL_NAME,
                                                            COLS_TO_AVG)


def get_daily_covid_data_from_file():
    """
    for use during testing (since the file download from s3 is slow)

    reads historical IDPH daily covid case data by zipcode from CSV
    returns data in pandas DataFrame
    """

    data = pd.read_csv(CSV_FILE_PATH)
    assert set(data.columns) == set(SELECT_COLUMNS)
    return data
