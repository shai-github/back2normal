from core.data import census_api_pull, data_transformations

ZIP_COL_NAME = data_transformations.STD_ZIP_COL_NAME


def test_get_census_data_from_api():
    
    census_df = census_api_pull.get_census_data_from_api()

    assert len(census_df) == 58
    data_transformations.standardize_zip_code_col(census_df, ZIP_COL_NAME)
    assert isinstance(census_df[census_api_pull.ZIP_COL_NAME][0], str)
