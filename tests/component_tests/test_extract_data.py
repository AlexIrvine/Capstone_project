import pandas as pd
from src.extract.extract import extract_data
from src.extract.create_file_list import create_file_list


# Tests the happy path of data extraction
def test_extract_data_happy_path():
    # Apply the function
    result = extract_data()
    # Check type return
    assert isinstance(result, dict)
    # Ensure it is not empty
    assert len(result) > 0
    # Manually do the file naming
    expected_files = []
    for path in create_file_list():
        file_name = path.name
        base_name = file_name.split(".", 1)[0]
        expected_files.append(base_name)
    # check the files are present
    for name in expected_files:
        assert name in result
    # Ensure dataframes are correct type and none empty
    for df in result.values():
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
