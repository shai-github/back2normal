"""
Module for creating sqlite database
"""
import os
import pandas as pd
from core.data import census_api_pull, dbclient, daily_case_data_by_zip, data_transformations
from core.data.socrata import soda_data, socrata_api_requests
from core.data.groundtruth import process_ground_truth_data

# Table names
VACC_TBL = soda_data.VACCINATION_DATA_OBJ.sql_table_name
CASE_TBL = daily_case_data_by_zip.SQL_TABLE_NM
FOOT_TRAFF_TBL = process_ground_truth_data.SQL_TABLE_NAME
CRASHES_TBL = "TRAFFIC_CRASH_DATA"
CENSUS_TBL = "DEMOGRAPHICS"


def build_back2normal_db():
    """
    Builds database from various datasources
    For each source:
        1. get data from source (API, CSV, etc) and convert to pandas DatFrame
        2. standardize zip code col name and format
        3. standardize date col name and format
        4. compute 7 day moving average
        5. create table in sqlite db
    """

    if os.path.exists(dbclient.DB_PATH):
        print("Deleting existing db and recreating with build_db_script\n")
        os.remove(dbclient.DB_PATH)
    db = dbclient.DBClient()

    # Vaccinations
    vacc_data_obj = soda_data.VACCINATION_DATA_OBJ
    vacc_api_resp = socrata_api_requests.SocrataAPIClient(vacc_data_obj.request_url)
    data_transformations.standardize_zip_code_col(vacc_api_resp.data_df, soda_data.VACC_ZIP_COL_NAME)
    data_transformations.standardize_date_col(vacc_api_resp.data_df, soda_data.VACC_DATE_COL_NAME)
    data_transformations.\
        compute_moving_avg_from_daily_data(vacc_api_resp.data_df,
                                           data_transformations.STD_ZIP_COL_NAME,
                                           data_transformations.STD_DATE_COL_NAME,
                                           vacc_data_obj.COLS_TO_AVG)
    db.create_table_from_pandas(vacc_api_resp.data_df, VACC_TBL)

    # DAILY COVID DATA BY ZIP from IDPH
    print("...Downloading daily Covid-19 data...")
    daily_covid_data = daily_case_data_by_zip.get_daily_covid_data_from_api()
    data_transformations.standardize_zip_code_col(daily_covid_data, daily_case_data_by_zip.ZIP_COL_NAME)
    data_transformations.standardize_date_col(daily_covid_data, daily_case_data_by_zip.DATE_COL_NAME)
    data_transformations.\
        compute_moving_avg_from_daily_data(daily_covid_data,
                                           data_transformations.STD_ZIP_COL_NAME,
                                           data_transformations.STD_DATE_COL_NAME,
                                           daily_case_data_by_zip.COLS_TO_AVG)
    db.create_table_from_pandas(daily_covid_data, CASE_TBL)

    # Ground truth foot traffic data
    daily_foot_traffic_data = process_ground_truth_data.get_combined_ground_truth_data()
    data_transformations.standardize_zip_code_col(
        daily_foot_traffic_data, process_ground_truth_data.ZIP_COL_NAME)
    data_transformations.standardize_date_col(daily_foot_traffic_data, process_ground_truth_data.DATE_COL_NAME)
    data_transformations.\
        compute_moving_avg_from_daily_data(daily_foot_traffic_data,
                                           data_transformations.STD_ZIP_COL_NAME,
                                           data_transformations.STD_DATE_COL_NAME,
                                           process_ground_truth_data.COLS_TO_AVG)
    db.create_table_from_pandas(daily_foot_traffic_data, FOOT_TRAFF_TBL)

    # SOCRATA CRASH DATA
    crash_file = os.path.join("core", "resources", "zipcode_crash_data_1_1_2019-3_7_20201.csv")
    crash_data = pd.read_csv(crash_file)
    data_transformations.standardize_zip_code_col(crash_data, soda_data.CRASH_ZIP_COL_NAME)
    data_transformations.standardize_date_col(crash_data, soda_data.CRASH_DATE_COL_NAME)
    data_transformations.\
        compute_moving_avg_from_daily_data(crash_data,
                                           data_transformations.STD_ZIP_COL_NAME,
                                           data_transformations.STD_DATE_COL_NAME,
                                           ['crash_count'])
    db.create_table_from_pandas(crash_data, CRASHES_TBL)

    # CENSUS Demographic Data
    census_data = census_api_pull.get_census_data_from_api()
    data_transformations.standardize_zip_code_col(census_data, census_api_pull.ZIP_COL_NAME)
    db.create_table_from_pandas(census_data, CENSUS_TBL)


if __name__ == "__main__":
    print(f"Building {dbclient.DB_PATH}")
    build_back2normal_db()
    print("Tables built successfully")
