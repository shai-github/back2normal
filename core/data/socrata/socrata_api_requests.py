"""
Class for managing Socrata get requests
"""
import requests
import pandas as pd
from core.util import api_util
from core.data import data_transformations


class SocrataAPIClient:
    """
    Class for making requests to Socrata Chicago API
    and parsing, updating the response object
    """

    def __init__(self, request_url):

        self.request_url = None
        self.params = self._get_app_token_params()
        self.response = None
        self.data_df = None

        # for reviewing datatypes
        self.header_fields = None
        self.header_dtypes = None

        self._get_request(request_url)

    @staticmethod
    def _get_app_token_params():
        """
        gets api token and formats the params dict for request
        :return: dict containing app token
        """
        token = api_util.get_socrata_app_token()
        return {"$$app_token": token}

    def _get_request(self, request_url):
        """
        sends get request to socrata api
        parses reponse header for debugging data types
        converse json response to a pandas DataFrame
        updates the data types in data_df, the pandas DataFrame containing the
        API response data

        Attempt to convert all fields to numeric types (float or integer)
        Then convert non numeric types back to string

        :param request_url: url for the get request
        :return: NA
        """
        # For header codes included in response object: 
        # https://dev.socrata.com/docs/response-codes.html

        # Difference between a Request and a Response object:
        # https://requests.readthedocs.io/en/master/user/advanced/#request-and-response-objects
        # get and parse response
        self.response = requests.get(request_url, self.params)
        self.request_url = self.response.request.url
        if self.response.status_code != 200:
            raise Exception(f"bad request: {self.request_url}")

        self.header_fields = self.response.headers['X-SODA2-Fields']
        self.header_dtypes = self.response.headers['X-SODA2-Types']

        # convert to pandas df
        self.data_df = pd.DataFrame.from_dict(self.response.json())

        # convert dtypes
        self.data_df = data_transformations.convert_df_dtypes(self.data_df)
