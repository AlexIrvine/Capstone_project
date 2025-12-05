import pytest
import geopy.distance
import pandas as pd
from pathlib import Path
from src.extract.extract_files_into_df import extract_files_to_df
from src.transform.clean_data import (
    remove_missing_values,
    ensure_datetime,
    distance_calculator,
    time_delta,
    remove_zero_time_delta,
    speed_calculation,
    remove_outliers,
    clean_data
)

# Set up pytests for coding
@pytest.fixture
def whale_data():
    root = Path(__file__).resolve().parents[1]

    test_data = [
        root / "test_data" / "Antarctic blue whales, east Antarctic sector of the Southern Ocean.csv",
        root / "test_data" / "Azores Great Whales Satellite Telemetry Program.csv",
        root / "test_data" / "Baffin Bay narwhal- 2009 to 2012 Argos data- Fisheries and Oceans Canada.csv",
    ]
    return extract_files_to_df(test_data)


@pytest.fixture
def whale_data_distance_calculated(whale_data: dict):
    whale_data_dc = remove_missing_values(whale_data)
    whale_data_dc = ensure_datetime(whale_data_dc)
    return distance_calculator(whale_data_dc)


@pytest.fixture
def whale_time_delta_calculated(whale_data_distance_calculated):
    return time_delta(whale_data_distance_calculated)

@pytest.fixture
def whale_zero_time_delta_run(whale_time_delta_calculated):
    return remove_zero_time_delta(whale_time_delta_calculated)

@pytest.fixture
def whale_speed_calculation_run(whale_zero_time_delta_run):
    return speed_calculation(whale_zero_time_delta_run)


class TestRemoveMissingValues:
    def test_remove_missing_values_success(self):
        # Keep only rows with all required columns present.
        df = pd.DataFrame(
            {
                "timestamp": ["2013-03-08 05:45:10", None, None,
                              "2013-03-12 18:58:55"],
                "location-lat": [-64.582, -64.592, -64.546, None],
                "location-long": [169.753, 169.753, None, 169.753],
                "individual-local-identifier": ["O", "W", None, "O"],
                "tag-local-identifier": ["K", "G", "T", "H"]

            }
        )

        data_dict = {"test": df}

        result = remove_missing_values(data_dict)

        cleaned = result["test"]

        # Should keep row 1
        assert len(cleaned) == 1
        assert cleaned.iloc[0]["location-long"] == 169.753

    def test_remove_missing_values_no_missing(self):
        # Test with DataFrame that has no missing values.
        # Set up fake data
        df = pd.DataFrame(
            {
                "timestamp": ["2013-03-08 05:45:10", "2013-03-12 18:58:55"],
                "location-lat": [-64.582, -64.592],
                "location-long": [169.753, 169.753],
                "individual-local-identifier": ["O", "W"],
                "tag-local-identifier": ["K", "H"],
            }
        )

        data_dict = {"test": df}

        result = remove_missing_values(data_dict)

        cleaned = result["test"]

        # Assures the length is whats expected and data is present
        assert len(cleaned) == 2
        assert cleaned.iloc[0]["timestamp"] == "2013-03-08 05:45:10"
        assert cleaned.iloc[1]["timestamp"] == "2013-03-12 18:58:55"

    def test_remove_missing_values(self, whale_data: dict):
        # Test on actual data
        actual = remove_missing_values(whale_data)
        for df in actual.values():
            na_count = (
                df[
                    [
                        "location-long",
                        "location-lat",
                        "timestamp",
                        "individual-local-identifier",
                        "tag-local-identifier"
                        ]
                    ].isna().sum().sum()
            )
            # If there are NAs it raises an error
            if na_count != 0:
                raise AssertionError("Nas present in the required columns")


class TestEnsureDateTime:
    def test_ensure_datetime_function_exists(self):
        # Test that ensure_datetime function exists and is callable.
        assert callable(ensure_datetime)

    def test_ensure_datetime_basic(self):
        # Test with fake data
        df = pd.DataFrame(
            {
                "timestamp": ["2013-03-08 05:45:10", "2013-03-12 18:58:55"],
                "location-lat": [-64.582, -64.592],
                "location-long": [169.753, 169.753],
                "individual-local-identifier": ["O", "W"],
                "tag-local-identifier": ["K", "H"],
            }
        )

        data_dict = {"TestWhale": df}

        actual = ensure_datetime(data_dict)
        # Tests they are all datetimes or throws an error
        for df in actual.values():
            assert "datetime" in str(df['timestamp'].dtype)

    def test_ensure_datetime_invalid_dates(self):
        # Test that invalid timestamp strings become Na.
        df = pd.DataFrame(
            {
                "timestamp": ["2013-03-08 05:45:10", "error"],
                "location-lat": [1, 2],
                "location-long": [3, 4],
                "individual-local-identifier": ["A", "A"],
                "tag-local-identifier": ["T1", "T1"],
            }
        )

        data_dict = {"Whale": df}

        actual = ensure_datetime(data_dict)
        actual = actual["Whale"]
        # Should be an Na
        assert pd.isna(actual["timestamp"].iloc[1])

    def test_ensure_datetime(self, whale_data):
        # Test on real data
        actual = remove_missing_values(whale_data)
        actual = ensure_datetime(actual)
        for df in actual.values():
            assert "datetime" in str(df['timestamp'].dtype)


class TestDistanceCalculation():
    def test_distance_calculator_first_row_zero(self):
        # Test first row is zero with fake data
        test_data = {
            "Test": pd.DataFrame({
                "event-id": [24174715705, 24174715706],
                "individual-local-identifier": ["121205", "121205"],
                "tag-local-identifier": ["121205", "121205"],
                "timestamp": pd.to_datetime([
                    "2013-03-08 11:24:04",
                    "2013-03-08 11:36:15"
                ]),
                "location-lat": [-64.217, -64.242],
                "location-long": [169.116, 169.103]
            })
        }

        actual = distance_calculator(test_data)
        df = actual["Test"]

        assert df.loc[0, "distance_from_prev_m"] == 0

    def test_distance_calculator_real_data(self):
        # Checks the geopy function works within the calculation
        df = pd.DataFrame({
            "event-id": [24174715705, 24174715706],
            "individual-local-identifier": ["121205", "121205"],
            "tag-local-identifier": ["121205", "121205"],
            "timestamp": pd.to_datetime([
                "2013-03-08 11:24:04",
                "2013-03-08 11:36:15"
            ]),
            "location-lat": [-64.217, -64.242],
            "location-long": [169.116, 169.103]
        })

        data_dict = {"TestDF": df}

        result = distance_calculator(data_dict)
        updated = result["TestDF"]

        expected = geopy.distance.distance(
            (-64.217, 169.116),
            (-64.242, 169.103)
        ).meters

        actual = updated.loc[1, "distance_from_prev_m"]

        assert actual == expected

    def test_distance_calculator_sorting(self, whale_data_distance_calculated):
        # Test that the sorting stage works correctly on actual data
        actual = whale_data_distance_calculated

        # For every data frame
        for df in actual.values():    
            # Check the number of unique identifiers:
            whale_tag_number_expected = (
                df[
                    [
                        "individual-local-identifier",
                        "tag-local-identifier",
                    ]
                ]
                .drop_duplicates()
                .shape[0]
            )
            # Set whale number to one to account for first row
            whale_tag_number_actual = 1

            # For every cell in the column
            for i in range(1, len(df)):
                # If the cell does not equal the one before another
                # whale is present
                if (
                    df.loc[i, "individual-local-identifier"]
                    != df.loc[i - 1, "individual-local-identifier"]
                    or
                    df.loc[i, "tag-local-identifier"]
                    != df.loc[i - 1, "tag-local-identifier"]
                ):
                    whale_tag_number_actual += 1

                same_group = (
                    df.loc[i, "individual-local-identifier"]
                    == df.loc[i - 1, "individual-local-identifier"]
                    and
                    df.loc[i, "tag-local-identifier"]
                    == df.loc[i - 1, "tag-local-identifier"]
                )

                # If whale is equal and the current time is less than the
                # previous their is an error
                if (
                    same_group
                    and df.loc[i, "timestamp"] < df.loc[i - 1, "timestamp"]
                ):
                    raise AssertionError("Timings in wrong order")

            assert whale_tag_number_actual == whale_tag_number_expected

    def test_distance_calculator_zero(self, whale_data_distance_calculated):
        '''
        Test distance is not anything when no previous value or
        start of a new whale
        '''
        actual = whale_data_distance_calculated

        for df in actual.values():
            for i in range(len(df)):

                # First row of entire dataset must be zero
                if i == 0 and df.loc[i, "distance_from_prev_m"] != 0:
                    raise AssertionError("Distance from prev does "
                                         "not start with zero")
                elif i == 0:
                    continue

                # Check if whale OR tag changed -> distance must reset to zero
                new_group = (
                    df.loc[i, "individual-local-identifier"] 
                    != df.loc[i-1, "individual-local-identifier"]
                    or
                    df.loc[i, "tag-local-identifier"]
                    != df.loc[i-1, "tag-local-identifier"]
                )

                if new_group and df.loc[i, "distance_from_prev_m"] != 0:
                    raise AssertionError(
                        "Distance from prev does not reset "
                        "to zero at new whale or tag"

                    )

    def test_distance_calculator_positive_number(self, whale_data_distance_calculated):
        # All distances must be none negative
        actual = whale_data_distance_calculated

        for df in actual.values():
            for i in range(1, len(df)):
                assert df.loc[i, "distance_from_prev_m"] >= 0

    # Test columns are the correct length as original
    def test_distance_column_same(self, whale_data_distance_calculated):

        actual = whale_data_distance_calculated
        for df in actual.values():
            assert len(df["distance_from_prev_m"]) == len(df)


# Testing time delta calculation
class TestTimeDeltaCalculation():
    # Test with fake data and known time calculation
    def test_time_delta_real_data(self):
        df = pd.DataFrame(
            {
                "individual-local-identifier": ["121205", "121205"],
                "tag-local-identifier": ["121205", "121205"],
                "timestamp": pd.to_datetime([
                    "2013-03-08 11:24:04",
                    "2013-03-08 11:36:15"
                    ]
                                            )
                }
            )

        data_dict = {"TestDF": df}

        actual = time_delta(data_dict)
        actual = actual["TestDF"]
        # First row 0 second known value
        assert actual.loc[0, "time_diff_s"] == 0
        assert actual.loc[1, "time_diff_s"] == 731

    # First row in every data frame must be 0
    def test_time_delta_first_zero(self, whale_data_distance_calculated):

        actual = time_delta(whale_data_distance_calculated)

        for df in actual.values():
            assert df.loc[0, "time_diff_s"] == 0

    def test_time_delta_new_whale_zero(self, whale_data_distance_calculated):
        # Whenever a new whale and tag starts time should be zero

        actual = time_delta(whale_data_distance_calculated)

        for df in actual.values():
            for i in range(1, len(df)):
                new_whale = (
                    df.loc[i, "individual-local-identifier"] !=
                    df.loc[i - 1, "individual-local-identifier"]
                )
                if new_whale and df.loc[i, "time_diff_s"] != 0:
                    raise AssertionError("New whale must start "
                                         "with 0 time difference")

    def test_time_delta_no_zeros(self, whale_time_delta_calculated):
        # Tets there should be no zeros in the whale data
        actual = remove_zero_time_delta(whale_time_delta_calculated)

        for df in actual.values():
            for i in range(1, len(df)):
                same_whale = (
                    df.loc[i, "individual-local-identifier"] ==
                    df.loc[i-1, "individual-local-identifier"]
                )
                if same_whale and df.loc[i, "time_diff_s"] == 0:
                    raise AssertionError("Zeros still present")


class SpeedCalculation():
    """
    Test that speed is not zero when time delat is not zero
    """
    def test_speed_zero_time(self, whale_zero_time_delta_run): 
        actual = speed_calculation(whale_zero_time_delta_run)

        for df in actual.values():
            zero_time_rows = df[df["time_diff_s"] == 0]
            if (zero_time_rows["speed_mps"] != 0).any():
                raise AssertionError("Speed is not zero when time delta is 0")

    # Test the speed column is the correct length
    def test_speed_column_same(self, whale_zero_time_delta_run):
        actual = speed_calculation(whale_zero_time_delta_run)

        for df in actual.values():
            assert len(df["speed_mps"]) == len(df)

    # Test no speed are negative
    def test_speed_non_negative(self, whale_zero_time_delta_run):
        actual = speed_calculation(whale_zero_time_delta_run)

        for df in actual.values():
            if (df["speed_mps"] < 0).any():
                raise AssertionError("Negative speeds present")

    # Test there are no Nas in the speed column
    def test_speed_no_nas(self, whale_zero_time_delta_run): 
        actual = speed_calculation(whale_zero_time_delta_run)

        for df in actual.values():
            if df["speed_mps"].isna().any():
                raise AssertionError("Speed calculation produced NaN values")


def test_outlier_removal_fake_data():
    # Test on fake data as real would not work.
    df = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2020-01-01 00:00:00",
            "2020-01-01 00:10:00",
            "2020-01-01 00:20:00"
        ]),
        "location-lat": [0, 0.1, 0.2],
        "location-long": [0, 0.1, 0.2],
        "individual-local-identifier": ["W1", "W1", "W1"],
        "tag-local-identifier": ["T1", "T1", "T1"],
        "speed_mps": [5, 12, 3]   
    })

    data_dict = {"TestWhale": df}

    result = remove_outliers(data_dict)
    cleaned_df = result["TestWhale"]
    assert len(cleaned_df) == 2 
    assert (cleaned_df["speed_mps"] > 10).sum() == 0   


def test_clean_data_end_to_end(whale_data):
    actual = clean_data(whale_data)

    # Should return a dict of DataFrames
    assert isinstance(actual, dict)
    for df in actual.values():
        # essential columns must exist after pipeline
        assert "distance_from_prev_m" in df.columns
        assert "time_diff_s" in df.columns
        assert "speed_mps" in df.columns

        # no missing timestamps after cleaning
        assert df["timestamp"].isna().sum() == 0

        '''
        Would like to test for no outliers but some still remain
        Future work!
        '''
