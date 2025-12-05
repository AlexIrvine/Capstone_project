import pandas as pd
import pytest
from pathlib import Path
from src.extract.extract_files_into_df import extract_files_to_df
from src.transform.clean_data import clean_data
from src.transform.create_new_df import create_combined_df
from src.transform.transform import transform_data


# Load the pytest data to run the full transformation
@pytest.fixture
def raw_whale_data():
    """Load 3 real CSVs exactly like the pipeline expects."""
    root = Path(__file__).resolve().parents[1] / "test_data"

    csvs = [
        root / "Antarctic blue whales, east Antarctic sector of the Southern Ocean.csv",
        root / "Azores Great Whales Satellite Telemetry Program.csv",
        root / "Baffin Bay narwhal- 2009 to 2012 Argos data- Fisheries and Oceans Canada.csv",
    ]

    return extract_files_to_df(csvs)


# Test required columns and no Nas in required columns
class TestTransformComponent:

    def test_clean_data_path(self, raw_whale_data):
        """
        clean_data should output a dict of cleaned DataFrames 
        with required columns.
        """
        cleaned = clean_data(raw_whale_data)

        assert isinstance(cleaned, dict)
        assert len(cleaned) == len(raw_whale_data)

        required_cols = [
            "timestamp",
            "location-lat",
            "location-long",
            "distance_from_prev_m",
            "time_diff_s",
            "speed_mps",
        ]

        # Check it is in columns
        # No Nas in required columns
        for df in cleaned.values():
            for col in required_cols:
                assert col in df.columns
                assert df[col].isna().sum() == 0

    def test_create_combined_df(self, raw_whale_data):
        """
        create_combined_df should combine 
        all cleaned frames into one full dataset.
        """
        cleaned = clean_data(raw_whale_data)
        combined = create_combined_df(cleaned)

        assert isinstance(combined, pd.DataFrame)
        assert len(combined) == sum(len(df) for df in cleaned.values())

        expected_cols = [
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
            "study_name",
        ]

        for col in expected_cols:
            assert col in combined.columns
            assert combined[col].isna().sum() == 0

    def test_transform_data_full_pipeline(self, raw_whale_data):
        final_df = transform_data(raw_whale_data)

        assert isinstance(final_df, pd.DataFrame)
        assert len(final_df) > 0
        assert final_df.isna().sum().sum() == 0

        essential = [
            "study_tag_id",
            "timestamp",
            "location_lat",
            "location_lon",
            "distance_from_prev_m",
            "time_diff_s",
            "speed_mps",
        ]

        # Check it is in columns
        # No Nas in required columns
        for col in essential:
            assert col in final_df.columns
            assert final_df[col].isna().sum() == 0
