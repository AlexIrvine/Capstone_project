import pandas as pd
import pytest
from pathlib import Path
from src.extract.extract_files_into_df import extract_files_to_df

# Set the path to the test data
root_tests = Path(__file__).resolve().parents[1]
test_data_directory = root_tests / "test_data"


# Make the file paths to the data as function wont work
@pytest.fixture
def file_list_for_tests():

    test_dir = Path(__file__).resolve().parents[1] / "test_data"

    file1 = (
        "Antarctic blue whales, east Antarctic sector of the "
        "Southern Ocean.csv"
    )
    file2 = "Azores Great Whales Satellite Telemetry Program.csv"
    file3 = (
        "Baffin Bay narwhal- 2009 to 2012 Argos data- "
        "Fisheries and Oceans Canada.csv"
    )

    return [test_dir / file1, test_dir / file2, test_dir / file3]


def test_extract_files_to_df(file_list_for_tests):
    # Apply the function
    result = extract_files_to_df(file_list_for_tests)
    # Test the function returns a dictionary and its the correct length
    assert isinstance(result, dict)
    assert len(result) == 3
    # Ensure it has converted to a dataframe
    for df in result.values():
        assert isinstance(df, pd.DataFrame)
        # Ensure they are not empty
        assert len(df) > 0


def test_extract_files_to_df_correct_keys(file_list_for_tests):
    # Call the function
    result = extract_files_to_df(file_list_for_tests)
    # Set the expected names
    expected_keys = [
        "Antarctic blue whales, east Antarctic sector of the Southern Ocean",
        "Azores Great Whales Satellite Telemetry Program",
        "Baffin Bay narwhal- 2009 to 2012 Argos data- "
        "Fisheries and Oceans Canada",
    ]
    # Ensure they are the same
    assert list(result.keys()) == expected_keys
