from core.data import data_transformations
from core.data.socrata import soda_data, socrata_api_requests
from core.util import api_util
import requests

#######################################################
####### SCRIPT FOR GRABBING ZIPCODES FR MAPBOX ########
#######################################################

# ~~~~~~ ******* Will not run without resource/location_zip.json ******* ~~~~~~ #


# Traffic Crashes (Historical 1/1/2019 00:00:00 to 3/7/2021 00:00:00
# in the future use a different (newer) dataset
data_obj = soda_data.TRAFFIC_CRASH_DATA_OBJ_HISTORICAL  # 1
api_resp = socrata_api_requests.SocrataAPIClient(data_obj.request_url)  # 2
data_df = api_resp.data_df

# save file just in case
# data_df.to_csv("historical_traffic_1_1_2019-3_7_20201.csv", index=False)


#######################################################
######## get zipcode from mapbox geocoding api ########
#######################################################
# requests are limited to 600 per minute

# continue processing from specified row
# row_to_start_processing = 155000
# subset_to_process = data_df.iloc[row_to_start_processing:]

# convert location to zip
access_token = api_util.get_mapbox_app_token()
session = requests.session()

zipcodes = []
for row_tuple in data_df.itertuples():
    print(row_tuple.Index)
    zipcodes.append(
        data_transformations.get_zipcode_from_mapbox(row_tuple.latitude,
                                                     row_tuple.longitude,
                                                     session,
                                                     access_token))
