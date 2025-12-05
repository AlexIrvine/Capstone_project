import pandas as pd
import pytest
from pathlib import Path
from src.extract.extract_files_into_df import extract_files_to_df
from src.transform.clean_data import clean_data
from src.transform.create_new_df import (
    create_combined_df,
    create_unique_column,
    retain_useful_columns,
    change_column_names,
    combined_df
)


# Load in the test data(reduced actual)
@pytest.fixture
def whale_data():
    root = Path(__file__).resolve().parents[1]

    test_data = [
        root / "test_data" / (
            "Antarctic blue whales, east Antarctic sector "
            "of the Southern Ocean.csv"
        ),
        root / "test_data" / (
            "Azores Great Whales Satellite Telemetry Program.csv"
        ),
        root / "test_data" / (
            "Baffin Bay narwhal- 2009 to 2012 Argos data- "
            "Fisheries and Oceans Canada.csv"
        ),
    ]

    return extract_files_to_df(test_data)


# Set up the pytest fixtures to follow along with the expected columns
@pytest.fixture
def whale_data_cleaned(whale_data):
    cleaned_data = clean_data(whale_data)
    return cleaned_data


@pytest.fixture
def cleaned_unique_col(whale_data_cleaned):
    whale_data_cleaned = create_unique_column(whale_data_cleaned)
    return whale_data_cleaned


@pytest.fixture
def retained_usuful_col(cleaned_unique_col):
    whale_data_cleaned = retain_useful_columns(cleaned_unique_col)
    return whale_data_cleaned


@pytest.fixture
def changed_col_names(retained_usuful_col):
    whale_data_cleaned = change_column_names(retained_usuful_col)
    return whale_data_cleaned


# Tests for unique column generation
class TestUniqueColumnGeneration():

    # Tests the study_id tag is structured correctly
    def test_create_unique_column(self):
        df = pd.DataFrame({
            "study-name": ["Blue Whale Study", "Humpback Whale Study"],
            "tag-local-identifier": ["Tag1", "Tag2"]
        })

        data = {"Test": df}

        actual = create_unique_column(data)
        actual = actual["Test"]

        # Asserts study_tag_id is in the column and it comes across correctly
        assert "study_tag_id" in actual.columns
        assert actual.loc[0, "study_tag_id"] == "Blue Whale Study_Tag1"
        assert actual.loc[1, "study_tag_id"] == "Humpback Whale Study_Tag2"

    # Ensure there are no NAs in the study_tag_id column
    def test_unique_column_na(self, whale_data_cleaned):
        # With actual data
        actual = create_unique_column(whale_data_cleaned)
        for df in actual.values():
            assert "study_tag_id" in df.columns
            assert df["study_tag_id"].isna().sum() == 0

    # Ensure the combined column is always a string
    def test_all_str(self, whale_data_cleaned):
        actual = create_unique_column(whale_data_cleaned)
        for df in actual.values():
            for i in range(len(df)):
                assert isinstance(df.loc[i, "study_tag_id"], str)


# Test required columns are retained
class TestRetainedColumns():
    # Perform a test to ensure it removes a column
    def test_retain_useful_columns(self):
        df = pd.DataFrame({
            "study_tag_id": ["121205", "121206"],
            "timestamp": ["2013-03-10 07:01:29", "2013-03-10 07:27:48"],
            "location-lat": [-64.191, -64.242],
            "location-long": [169.181, 169.689],
            "distance_from_prev_m": [0, 5.9],
            "time_diff_s": [0, 10.5],
            "speed_mps": [0, 0.5],
            "individual-local-identifier": ["121205", "121206"],
            "tag-local-identifier": ["T1", "T2"],
            "individual-taxon-canonical-name": ["Species1", "Species2"],
            "study-name": ["Balaenoptera musculus", "Balaenoptera musculus"],
            "test_col": [999, "Test"]
        })

        data = {"Test": df}

        actual = retain_useful_columns(data)
        actual_df = actual["Test"]
        # The expected columns
        expected_cols = [
            "study_tag_id",
            "timestamp",
            "location-lat",
            "location-long",
            "distance_from_prev_m",
            "time_diff_s",
            "speed_mps",
            "individual-local-identifier",
            "tag-local-identifier",
            "individual-taxon-canonical-name",
            "study-name"
        ]

        # Compare the list of columns
        assert list(actual_df.columns) == expected_cols
        # Check the specific column is not in
        assert "test_col" not in actual_df.columns
        # Check the length is correct
        assert len(actual_df) == 2

    # Ensure there are no Na values in required fields
    def test_no_nas(self, cleaned_unique_col):
        actual = retain_useful_columns(cleaned_unique_col)

        expected_cols = [
            "study_tag_id",
            "timestamp",
            "location-lat",
            "location-long",
            "distance_from_prev_m",
            "time_diff_s",
            "speed_mps",
            "individual-local-identifier",
            "tag-local-identifier",
            "individual-taxon-canonical-name",
            "study-name"
        ]

        for df in actual.values():
            assert list(df.columns) == expected_cols
            na_count = df[expected_cols].isna().sum().sum()
            assert na_count == 0


# Test column renaming logic
class TestColumnNameChange():

    # Test to see it removes a column
    def test_change_col_name(self):
        df = pd.DataFrame({
            "study_tag_id": ["121205", "121206"],
            "timestamp": ["2013-03-10 07:01:29", "2013-03-10 07:27:48"],
            "location-lat": [-64.191, -64.242],
            "location-long": [169.181, 169.689],
            "distance_from_prev_m": [0, 5.9],
            "time_diff_s": [0, 10.5],
            "speed_mps": [0, 0.5],
            "individual-local-identifier": ["121205", "121206"],
            "tag-local-identifier": ["T1", "T2"],
            "individual-taxon-canonical-name": ["Species1", "Species2"],
            "study-name": ["Balaenoptera musculus", "Balaenoptera musculus"],
            "test_col": [999, "Test"]
        })

        data = {"Test": df}

        actual = change_column_names(data)
        actual = actual["Test"]

        expected_cols = [
            "location_lat",
            "location_lon",
            "individual_local_identifier",
            "tag_local_identifier",
            "individual_taxon_canonical_name",
            "study_name"
        ]

        # Check the columns against expected
        for col in expected_cols:
            assert col in actual.columns

        old_cols = [
            "location-lat",
            "location-long",
            "individual-local-identifier",
            "tag-local-identifier",
            "individual-taxon-canonical-name",
            "study-name"
        ]

        # Check the old columns still are not in there
        for col in old_cols:
            assert col not in actual.columns

    # Test renaming with real data
    def test_change_col_names_real(self, retained_usuful_col):
        actual = change_column_names(retained_usuful_col)

        expected_cols = [
            "location_lat",
            "location_lon",
            "individual_local_identifier",
            "tag_local_identifier",
            "individual_taxon_canonical_name",
            "study_name"
        ]

        # Check the columns against expected
            
        for col in expected_cols:
            for df in actual.values():
                assert col in df.columns


def test_combined_df_real(changed_col_names):
    actual = combined_df(changed_col_names)

    # number of rows after merging should equal sum of source dfs
    expected_len = sum(len(df) for df in changed_col_names.values())

    assert len(actual) == expected_len

    # ensure no missing essential columns
    essential = [
        "study_tag_id",
        "timestamp",
        "location_lat",
        "location_lon",
        "distance_from_prev_m",
        "time_diff_s",
        "speed_mps",
        "individual_local_identifier",
        "tag_local_identifier",
        "individual_taxon_canonical_name",
        "study_name"
    ]
    for col in essential:
        assert col in actual.columns


def test_create_combined_df(changed_col_names):
    actual = combined_df(changed_col_names)

    # Should return a dict of DataFrames
    assert isinstance(actual, pd.DataFrame)


def test_full_combination(whale_data_cleaned):
    actual = create_combined_df(whale_data_cleaned)

    assert isinstance(actual, pd.DataFrame)
    assert len(actual) > 0

    expected_len = sum(len(df) for df in whale_data_cleaned.values())
    assert len(actual) == expected_len
