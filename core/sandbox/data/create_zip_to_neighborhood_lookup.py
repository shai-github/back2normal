"""
Script for creating dict of zip to neighborhood name list
based on data from
https://www.chicagotribune.com/chi-community-areas-htmlstory.html
"""
import os
from core.util import basic_io

path_to_neighborhood_csv = os.path.join("core", "resources", "chicago_neighborhoods.csv")
zip_data = basic_io.read_csv_to_list(path_to_neighborhood_csv)
zip_data.pop(0)
zip_dict = {}
zip_col = 0
neighborhoods_col = 1
for row in zip_data:
    zip_dict[str(row[0])] = str(row[1])

basic_io.write_dict_to_json("chicago_neighborhoods.js", zip_dict)


