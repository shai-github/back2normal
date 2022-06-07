from datetime import datetime
from core.util import basic_io

# https://strftime.org/ python datetime formats
# file on my local - not a fan of storing stuff like this in git
# data from https://ibis.health.state.nm.us/resource/MMWRWeekCalendar.html#part3
data = basic_io.read_csv_to_list("/Users/christineibaraki/Desktop/CDC_MMWR_Weeks.csv")
WEEK_COL = 0


def create_dict_for_row(row):
    result = {}
    week_value = int(row[WEEK_COL])
    assert 1 <= week_value <= 53
    for date_str in row[WEEK_COL+1:]:
        if not not date_str:
            date_obj = datetime.strptime(date_str, '%m/%d/%y')
            date_str_format = date_obj.strftime("%Y-%m-%d")
            result[date_str_format] = week_value
    return result


week_ending_to_cdc_week_dict = {}
for row in data:
    row_dict = create_dict_for_row(row)
    week_ending_to_cdc_week_dict.update(row_dict)

assert week_ending_to_cdc_week_dict["2020-05-02"] == 18
assert week_ending_to_cdc_week_dict["2023-04-15"] == 15
assert week_ending_to_cdc_week_dict["2024-12-28"] == 52
assert week_ending_to_cdc_week_dict["2026-01-03"] == 53
assert week_ending_to_cdc_week_dict["2022-01-01"] == 52
assert week_ending_to_cdc_week_dict["2016-01-09"] == 1
assert week_ending_to_cdc_week_dict["2018-04-07"] == 14
assert week_ending_to_cdc_week_dict["2021-01-02"] == 53

basic_io.write_dict_to_json('/Users/christineibaraki/Desktop/cdc_week.json',
                            week_ending_to_cdc_week_dict)
