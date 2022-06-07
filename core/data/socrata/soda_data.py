"""
Data object for Socrata Chicago Data
"""

VACC_ZIP_COL_NAME = 'zip_code'
VACC_DATE_COL_NAME = 'date'

CRASH_ZIP_COL_NAME = 'zipcode'
CRASH_DATE_COL_NAME = 'short_date'


class SodaData:
    """
    Data object for managing/storing fields related to a Socrata dataset.

    This class builds a socrata request url using a soql query.
    The request can be made via data/socrata_api_requests

    """

    def __init__(self, dataset_name, sql_table_name, identifier,
                 desired_attr_lst,
                 week_avg_attr_lst=None,
                 group_by=None,
                 where=None,
                 limit=None):
        """
        Constructor for SodaData

            dataset_name: (str) internal/informal name for data set
            sql_table_name: (str) table name in sqlite db
            identifier: (str) socrata ID
            desired_attr_list: list of (str) where each item represents
                a field in the soql select statement
            week_avg_attr_lst: list of (str) that should be a subset of
                desired_attr_list. represents fields on which to compute a weekly avg.
            group_by = (str) name of field to groupby in soql query
            where = (str) where statements for soql query
            limit = (int) number of rows on which to limit soql query
        """

        self.dataset_name = dataset_name
        self.sql_table_name = sql_table_name
        self.identifier = identifier

        # constructing api query
        self.base_url = f"https://data.cityofchicago.org/resource/{identifier}.json"
        self.desired_attr_lst = desired_attr_lst
        self.group_by_lst = group_by
        self.where_lst = where
        self.limit = limit

        # api request url
        self.request_url = self._build_soql_query()

        # variables for which weekly averages will be computed
        self.COLS_TO_AVG = week_avg_attr_lst

    def _build_soql_query(self):
        """
        builds a soql query to append to base request url.

        :return: (str) socrata api request url
        """

        # soql docs: https://dev.socrata.com/docs/queries/

        query =  f"?$query=SELECT {', '.join(self.desired_attr_lst)}"
        if self.where_lst:
            query += f" WHERE {'AND '.join(self.where_lst)}"
        if self.group_by_lst:
            query += f" GROUP BY {', '.join(self.group_by_lst)}"
        if self.limit:
            query += f" LIMIT {self.limit}"

        return self.base_url + query


############################################
######## COVID-19 Vaccinations by ZIP Code
############################################

# https://dev.socrata.com/foundry/data.cityofchicago.org/553k-3xzc
VACCINATION_DATA_OBJ = SodaData("COVID-19 Vaccinations by ZIP Code",
                         "VACCINATIONS",
                         "553k-3xzc",
                         [VACC_ZIP_COL_NAME , VACC_DATE_COL_NAME,
                          "total_doses_daily", "total_doses_cumulative",
                          "vaccine_series_completed_daily",
                          "vaccine_series_completed_percent_population",
                          "population"],
                         ["total_doses_daily", "vaccine_series_completed_daily"],
                         None,
                         None,
                         5000)

TRAFFIC_CRASH_DATA_OBJ_HISTORICAL = SodaData("Traffic Crashes",
                              "TRAFFIC_CRASHES",
                              "85ca-t3if",
                              ["CRASH_RECORD_ID", "CRASH_DATE",
                               "latitude", "longitude"],
                              where=["CRASH_DATE > '2019-01-01T00:00:00'",
                                     "CRASH_DATE < '2021-03-07T00:00:00'"],
                              limit=300000)
