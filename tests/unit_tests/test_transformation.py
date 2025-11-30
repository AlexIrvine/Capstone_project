from pathlib import Path
from datetime import datetime
from src.transform.clean_data import remove_missing_values
from src.transform.clean_data import test_ensure_datetime
from src.extract.extract_files_into_df import extract_files_to_df

actual = None


def test_remove_missing_values(): 
    
    root = Path(__file__).resolve().parents[1]
    
    test_data = sorted([
        root / "test_data" / "Antarctic blue whales, east Antarctic sector of the Southern Ocean.csv",
        root / "test_data" / "Azores Great Whales Satellite Telemetry Program.csv",
        root / "test_data" / "Baffin Bay narwhal- 2009 to 2012 Argos data- Fisheries and Oceans Canada.csv",
    ])
    
    data_frames = extract_files_to_df(test_data)
    
    actual = remove_missing_values(data_frames)
    
    for df in actual.values():
        na_count = df[["location-long", "location-lat", "timestamp", "individual-local-identifier"]].isna().sum().sum()
        if na_count != 0:
            raise AssertionError("Nas present in the required columns")


def test_ensure_datetime(data_dict):
    
    actual = test_ensure_datetime(actual)
    
    for df in actual.values():
        if not isinstance(df['timestamp'], datetime):
            raise AssertionError("None dataframe present")
        

 

    
    
    
    
   