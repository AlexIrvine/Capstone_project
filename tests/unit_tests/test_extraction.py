from pathlib import Path
import pandas as pd
from src.extract.create_file_list import create_file_list
from src.extract.extract_files_into_df import extract_files_to_df


def test_file_extraction_folder_access():
    
    expected_output = "C:\\Users\\alexj\\OneDrive\\Data_Engineering\\Assignments\\Capstone_project\\Capstone_project\\data\\raw"

    root_directory = Path(__file__).resolve().parents[2]
    
    actual_output = root_directory / "data" / "raw"
    
    assert expected_output == str(actual_output)
    
    
def test_file_list_extraction():
    root = Path(__file__).resolve().parents[2]

    actual = create_file_list()
    
    expected = [
        root / "data" / "raw" / "Antarctic blue whales, east Antarctic sector of the Southern Ocean.csv",
        root / "data" / "raw" / "Azores Great Whales Satellite Telemetry Program.csv",
        root / "data" / "raw" / "Baffin Bay narwhal- 2009 to 2012 Argos data- Fisheries and Oceans Canada.csv",
        root / "data" / "raw" / "Blue and fin whales Southern California 2014-2015 - Argos data.csv",
        root / "data" / "raw" / "Blue and fin whales Southern California 2014-2015 - Fastloc GPS data.csv",
        root / "data" / "raw" / "Blue whales Eastern North Pacific 1993-2008 - Argos data.csv",
        root / "data" / "raw" / "Blue whales Eastern North Pacific 2003 State-space model output.csv",
        root / "data" / "raw" / "Bowhead whale Admiralty Inlet.csv",
        root / "data" / "raw" / "Bowhead whale Cumberland Sound.csv",
        root / "data" / "raw" / "Bowhead whale Foxe Basin.csv",
        root / "data" / "raw" / "False Killer Whales - Hawaiian Islands- PIFSC.csv",
        root / "data" / "raw" / "Fin whales Gulf of California 2001 - Argos data.csv",
        root / "data" / "raw" / "Humpback whale and climate change.csv",
        root / "data" / "raw" / "Movements of Australia's east coast humpback whales.csv",
        root / "data" / "raw" / "Short-finned pilot whales CRC NW Atlantic.csv",
        root / "data" / "raw" / "Sperm whales Gulf of California 2007-2008 ADB Tags Argos data.csv",
        root / "data" / "raw" / "Sperm whales Gulf of Mexico 2011-2013 ADB Tags - Argos data.csv",
        root / "data" / "raw" / "Whale shark movements in Gulf of Mexico.csv",
    ]

    assert actual == expected


def test_extract_files_to_df():
    root = Path(__file__).resolve().parents[1]
    
    test_data = sorted([
        root / "test_data" / "Antarctic blue whales, east Antarctic sector of the Southern Ocean.csv",
        root / "test_data" / "Azores Great Whales Satellite Telemetry Program.csv",
        root / "test_data" / "Baffin Bay narwhal- 2009 to 2012 Argos data- Fisheries and Oceans Canada.csv",
    ])
    
    actual = extract_files_to_df(test_data)
    
    assert len(actual) == len(test_data)
    
    assert list(actual.keys()) == [
        "Antarctic blue whales, east Antarctic sector of the Southern Ocean",
        "Azores Great Whales Satellite Telemetry Program",
        "Baffin Bay narwhal- 2009 to 2012 Argos data- Fisheries and Oceans Canada",
    ]

    for df in actual.values():
        if not isinstance(df, pd.DataFrame):
            raise AssertionError("None dataframe present")
