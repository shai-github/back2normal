from core.data.socrata import soda_data, socrata_api_requests


def test_soda_data_groupby_query():

    soda_obj_groupby_query = soda_data.SodaData("Traffic Crashes - Crashes",
                                                "TRAFFIC_CRASHES",
                                                "85ca-t3if",
                                                ["COUNT(CRASH_RECORD_ID)", "CRASH_DATE"],
                                                group_by=['CRASH_DATE'],
                                                limit=100)

    api_resp_groupby = socrata_api_requests.SocrataAPIClient(soda_obj_groupby_query.request_url)

    correct_query = "https://data.cityofchicago.org/resource/85ca-t3if.json" \
                    "?$query=SELECT COUNT(CRASH_RECORD_ID), " \
                    "CRASH_DATE GROUP BY CRASH_DATE LIMIT 100"

    assert correct_query == soda_obj_groupby_query.request_url
    assert api_resp_groupby.response.status_code == 200


def test_soda_data_groupby_and_where_query():
    soda_obj_complex_query = soda_data.SodaData("Traffic Crashes - Crashes",
                                                "TRAFFIC_CRASHES",
                                                "85ca-t3if",
                                                ["COUNT(CRASH_RECORD_ID)", "CRASH_DATE"],
                                                group_by=['CRASH_DATE'],
                                                where=["CRASH_DATE > '2020-01-01T14:00:00'"],
                                                limit=100)

    api_resp_complex = socrata_api_requests.SocrataAPIClient(soda_obj_complex_query.request_url)

    correct_query = "https://data.cityofchicago.org/resource/85ca-t3if.json" \
                    "?$query=SELECT COUNT(CRASH_RECORD_ID), CRASH_DATE WHERE " \
                    "CRASH_DATE > '2020-01-01T14:00:00' GROUP BY CRASH_DATE LIMIT 100"

    assert correct_query == soda_obj_complex_query.request_url
    assert api_resp_complex.response.status_code == 200
