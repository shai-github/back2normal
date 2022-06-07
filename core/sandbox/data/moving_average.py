from core.data import data_transformations
from core.data.socrata import soda_data, socrata_api_requests

daily_vacc_data = soda_data.datasets[0]
response = socrata_api_requests.SocrataAPIClient(daily_vacc_data.request_url)
response.data_df

daily_data_df = response.data_df
# daily_data_df.sort_values(date_col_name, inplace = True)

# zipcode_col_name = 'zip_code'
# date_col_name = 'date'
# cols_to_avg = ['total_doses_daily']
# col_name = 'total_doses_daily'
# daily_data_df.groupby(zipcode_col_name)[col_name].rolling(window = 7).mean()
# daily_data_df.groupby(zipcode_col_name)[col_name].rolling(window = 7).mean()
# daily_data_df[new_col_name] = daily_data_df.groupby(zipcode_col_name)[col_name].rolling(window = 7).mean().reset_index(level = 0, drop=True)

data_transformations.compute_moving_avg_from_daily_data(daily_data_df, 'zip_code', 'date', ['total_doses_daily'])

print(daily_data_df[daily_data_df['zip_code' == "60637"]])