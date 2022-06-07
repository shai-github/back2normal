import requests
import math
import pandas as pd
from core.data import data_transformations
from core.data.socrata import soda_data
from core.util import basic_io, api_util

#######################################################
####### SCRIPT FOR CREATING TRAFFIC CRASH DATA ########
# this takes about 2-3 hours to run,
# since loc_to_zip_dict does not contain all locations
#######################################################

data_df = pd.read_csv("historical_traffic_1_1_2019-3_7_20201.csv")

loc_to_zip_dict = basic_io.read_json_to_dict(data_transformations.LOC_ZIP_FILE_PATH)
session = requests.Session()
access_token = api_util.get_mapbox_app_token()


def get_zip_from_dict_or_api(lat, long, session, app_token):

    if math.isnan(lat) or math.isnan(long) or lat == 0.0 or long == 0.0:
        return None

    location = repr((long, lat))
    if location in loc_to_zip_dict:
        return loc_to_zip_dict[location]
    print(location)
    return data_transformations.get_zipcode_from_lat_long(
        lat=lat, long=long,
        session=session, access_token=app_token)


output_file_name = "zip_code_location_mapbox_data_1_1_2019-3_7_20201.csv"

# write zipcode data while processing
# should have added crash date to the file
# only run this when need to retreive new zipcodes from mapbox
"""with open(output_file_name, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row_tuple in data_df.itertuples():
            zipcode = get_zip_from_dict_or_api(
                row_tuple.latitude,
                row_tuple.longitude,
                session,
                access_token)
            writer.writerow([row_tuple.Index, row_tuple.latitude, row_tuple.longitude, zipcode])
"""

########################################################
# build crash by zipcode dataset

result_header = list(data_df.columns)
result_header.insert(0, 'ORIG_INDEX')
result_header.append(soda_data.CRASH_ZIP_COL_NAME)

data_list = []
zipcode_data = basic_io.read_csv_to_list(output_file_name)
zipcode_data_index_col = 0
zipcode_data_lat_col = 1
zipcode_data_long_col = 2
zipcode_data_zipcol = 3

assert len(zipcode_data) == len(data_df)

for row_tuple in data_df.itertuples():
    zip_row = zipcode_data[row_tuple.Index]
    assert int(zip_row[zipcode_data_index_col]) == row_tuple.Index
    assert zip_row[zipcode_data_lat_col][0:10] == str(row_tuple.latitude)[0:10]
    assert zip_row[zipcode_data_long_col][0:10] == str(row_tuple.longitude)[0:10]
    new_row = list(row_tuple)
    new_row.append(zip_row[zipcode_data_zipcol])
    data_list.append(new_row)

assert len(data_list) == len(data_df)
assert len(data_list) == len(zipcode_data)

zipcode_crash_df = pd.DataFrame(data_list, columns=result_header)

pd.set_option('display.max_columns', None)
# data_df.zipcode.isna().sum()
# data_df_subset = data_df.loc[data_df.zipcode.isna() == False, ]

zipcode_crash_df[soda_data.CRASH_DATE_COL_NAME] = zipcode_crash_df['CRASH_DATE'].apply(lambda x: x[0:x.find("T")])

# for sanity checks
zipcode_crash_df.to_csv("zipcode_crashes_qa_1_1_2019-3_7_20201.csv", index=False)

zipcode_crash_counts = pd.DataFrame(zipcode_crash_df.value_counts(subset=[soda_data.CRASH_DATE_COL_NAME,
                                                                          soda_data.CRASH_ZIP_COL_NAME]))
zipcode_crash_counts.reset_index(inplace=True)
zipcode_crash_counts.columns = [soda_data.CRASH_DATE_COL_NAME,
                                soda_data.CRASH_ZIP_COL_NAME, 'crash_count']
zipcode_crash_counts.to_csv("zipcode_crash_data_1_1_2019-3_7_20201.csv", index=False)
