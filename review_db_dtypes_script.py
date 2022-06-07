import os
import pandas as pd
from core.data import census_api_pull, dbclient, daily_case_data_by_zip, data_transformations
from core.data.socrata import soda_data, socrata_api_requests
from core.data.groundtruth import process_ground_truth_data

pd.set_option('display.max_columns', None)

# Script to demonstrate how classes interact with each other
if os.path.exists(dbclient.DB_PATH_TEST):
    print("Deleting existing db and creating a new one for demo purposes\n")
    os.remove(dbclient.DB_PATH_TEST)
db = dbclient.DBClient(db_path=dbclient.DB_PATH_TEST)

# SOCRATA DATA PROCESS [data from https://data.cityofchicago.org]
# 1. get SodaData obj (representing single dataset) from soda_data global const
# 2. use SocrataAPIClient to get dataset, using SodaData.request_url
#    this returns a json that is converted to pandas dataframe
#    by default, all data values are of type str
# 3. standardize
# 4. compute weekly averages
# 5. use dbclient to create sql table from the pandas df

# Vaccinations
data_obj = soda_data.VACCINATION_DATA_OBJ  # 1
print(f" ##### making api request and create table for {data_obj.dataset_name} ####")
print(f"    sqlite table will be named {data_obj.sql_table_name}")
api_resp = socrata_api_requests.SocrataAPIClient(data_obj.request_url)  # 2
data_transformations.standardize_zip_code_col(api_resp.data_df, soda_data.VACC_ZIP_COL_NAME)  # 3
data_transformations.standardize_date_col(api_resp.data_df, soda_data.VACC_DATE_COL_NAME)
data_transformations.\
    compute_moving_avg_from_daily_data(api_resp.data_df,
                                       data_transformations.STD_ZIP_COL_NAME,  # should store this
                                       data_transformations.STD_DATE_COL_NAME,  # this too
                                       data_obj.COLS_TO_AVG)  # 4
db.create_table_from_pandas(api_resp.data_df, data_obj.sql_table_name)  # 5
print(f"    request url: {api_resp.request_url}")
print(f"    request headers {api_resp.header_fields}")
print(f"    request header dtypes {api_resp.header_dtypes}")
print("~~~~ pandas df dtypes ~~~~")
print(api_resp.data_df.dtypes)
print("~~~~ sql table info ~~~~~")
print(db.get_table_info(data_obj.sql_table_name))
print(f"nrow df:{len(api_resp.data_df)}\n")
print(api_resp.data_df.tail())


# DAILY COVID DATA BY ZIP
# [data from https://il-covid-zip-data.s3.us-east-2.amazonaws.com/latest/zips.csv]
# 1. use function get daily covid dataset as pandas df
#    if testing = True, data is read from csv resource
# 2. standardize
# 3. compute weekly average columns
# 4. use dbclient to create sql table from pandas df

daily_covid_data = daily_case_data_by_zip.get_daily_covid_data_from_api(testing=True)  # 1
data_transformations.standardize_zip_code_col(daily_covid_data, daily_case_data_by_zip.ZIP_COL_NAME)  # 2
data_transformations.standardize_date_col(daily_covid_data, daily_case_data_by_zip.DATE_COL_NAME)
data_transformations.\
    compute_moving_avg_from_daily_data(daily_covid_data,
                                       data_transformations.STD_ZIP_COL_NAME,
                                       data_transformations.STD_DATE_COL_NAME,
                                       daily_case_data_by_zip.COLS_TO_AVG)  # 3
print(daily_covid_data.tail())
db.create_table_from_pandas(daily_covid_data, daily_case_data_by_zip.SQL_TABLE_NM)  # 4
print("\nDAILY COVID DATA Table Info")
print(db.get_table_info(daily_case_data_by_zip.SQL_TABLE_NM))

# GROUND TRUTH Foot Traffic Data BY ZIP
# 1. use function to read in and combine ground truth CSVs
#    this returns a single pandas dataframe
# 2. standardize
# 3. compute weekly average columns
# 4. use dbclient to create sql table from pandas df

daily_foot_traffic_data = process_ground_truth_data.get_combined_ground_truth_data()  # 1
data_transformations.standardize_zip_code_col(
    daily_foot_traffic_data, process_ground_truth_data.ZIP_COL_NAME)  # 2
data_transformations.standardize_date_col(daily_foot_traffic_data, process_ground_truth_data.DATE_COL_NAME)
data_transformations.\
    compute_moving_avg_from_daily_data(daily_foot_traffic_data,
                                       data_transformations.STD_ZIP_COL_NAME,
                                       data_transformations.STD_DATE_COL_NAME,
                                       process_ground_truth_data.COLS_TO_AVG)
db.create_table_from_pandas(daily_foot_traffic_data, process_ground_truth_data.SQL_TABLE_NAME)  # 3

print("\nDAILY FOOT TRAFFIC Table Info")
print(db.get_table_info(process_ground_truth_data.SQL_TABLE_NAME))  # 4


# SOCRATA CRASH DATA
# THIS IS FOR TESTING/DATA EXPLORATION ONLY
# file for computing counts and creating this test csv is:
#       sandbox/data/create_zipcode_crash_for_testing.py
# file for processing the traffic data and getting zipcode from mapbox api:
#       process_traffic_crash_data.py
# date is 2019-11-12, (obj)
traffic_crash_sql_table_name = "TRAFFIC_CRASH_DATA"
crash_file = os.path.join("core", "resources", "zipcode_crash_data_1_1_2019-3_7_20201.csv")
crash_data = pd.read_csv(crash_file)
data_transformations.standardize_zip_code_col(crash_data, soda_data.CRASH_ZIP_COL_NAME)  # 2
data_transformations.standardize_date_col(crash_data, soda_data.CRASH_DATE_COL_NAME)
data_transformations.\
    compute_moving_avg_from_daily_data(crash_data,
                                       data_transformations.STD_ZIP_COL_NAME,
                                       data_transformations.STD_DATE_COL_NAME,
                                       ['crash_count'])  # 3
db.create_table_from_pandas(crash_data, traffic_crash_sql_table_name)  # 4

print("\nDAILY TRAFFIC CRASH Table Info")
print(db.get_table_info(traffic_crash_sql_table_name))

# CENSUS Data
census_df = census_api_pull.get_census_data_from_api()
data_transformations.standardize_zip_code_col(census_df, census_api_pull.ZIP_COL_NAME)

# make it easier to review datas
vacc_data = api_resp.data_df
case_data = daily_covid_data
groundtruth_data = daily_foot_traffic_data
traffic_crash_data = crash_data
data_list = [vacc_data, case_data, groundtruth_data, traffic_crash_data]
for x in data_list:
    print("\n\n")
    print(x.columns)
    print(f"\nzip col type = {x[data_transformations.STD_ZIP_COL_NAME].dtype}")
    print(f"\ndate col type = {x[data_transformations.STD_DATE_COL_NAME].dtype}")
    print(x[data_transformations.STD_DATE_COL_NAME].head(n=10))

census_data = census_df
