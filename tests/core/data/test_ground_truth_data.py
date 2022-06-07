from core.data.groundtruth import process_ground_truth_data


def test_clean_col_name():

    assert process_ground_truth_data.clean_col_name("arts & crafts") == "ARTS_CRAFTS"
    assert process_ground_truth_data.clean_col_name("arts_crafts") == "ARTS_CRAFTS"
    assert process_ground_truth_data.clean_col_name("arts  &  crafts") == "ARTS_CRAFTS"
