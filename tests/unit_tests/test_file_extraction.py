from pathlib import Path
from src.extract.create_file_list import create_file_list


def test_file_extraction_folder_access():
    # Define the expected output for file path
    expected_output = (
        "C:\\Users\\alexj\\OneDrive\\Data_Engineering\\"
        "Assignments\\Capstone_project\\Capstone_project\\data\\raw"
    )
    # Get the root path
    root_directory = Path(__file__).resolve().parents[2]
    # Combine it to the actual output test
    actual_output = root_directory / "data" / "raw"
    # Check the file logic works
    assert expected_output == str(actual_output)


def test_extract_csv_to_path_list(mocker):
    # Define some mock data files
    mock_files = ["File1.csv", "!@#%($%_)DCJE.csv", "Whales are cool.txt"]
    # Put the mock files in their place
    mocker.patch(
        "src.extract.create_file_list.os.listdir",
        return_value=mock_files)
    # Ensures the files wiithout a path pass in the code
    mocker.patch(
        "pathlib.Path.exists",
        return_value=True
    )

    # Call the function
    file_list = create_file_list()

    # Asser only the two csv should pass
    assert isinstance(file_list, list)
    assert len(file_list) == 2


def test_file_list_extraction():
    # Use the root now it works
    root = Path(__file__).resolve().parents[2]
    # Call the function
    actual = create_file_list()
    # Hard code the expected
    expected = [
        root / "data" / "raw" / (
            "Antarctic blue whales, east Antarctic sector of the "
            "Southern Ocean.csv"
        ),
        root / "data" / "raw" / (
            "Azores Great Whales Satellite Telemetry Program.csv"
        ),
        root / "data" / "raw" / (
            "Baffin Bay narwhal- 2009 to 2012 Argos data- Fisheries "
            "and Oceans Canada.csv"
        ),
        root / "data" / "raw" / (
            "Blue and fin whales Southern California 2014-2015 - "
            "Argos data.csv"
        ),
        root / "data" / "raw" / (
            "Blue and fin whales Southern California 2014-2015 - "
            "Fastloc GPS data.csv"
        ),
        root / "data" / "raw" / (
            "Blue whales Eastern North Pacific 1993-2008 - Argos data.csv"
        ),
        root / "data" / "raw" / (
            "Blue whales Eastern North Pacific 2003 State-space "
            "model output.csv"
        ),
        root / "data" / "raw" / "Bowhead whale Admiralty Inlet.csv",
        root / "data" / "raw" / "Bowhead whale Cumberland Sound.csv",
        root / "data" / "raw" / "Bowhead whale Foxe Basin.csv",
        root / "data" / "raw" / (
            "False Killer Whales - Hawaiian Islands- PIFSC.csv"
        ),
        root / "data" / "raw" / (
            "Fin whales Gulf of California 2001 - Argos data.csv"
        ),
        root / "data" / "raw" / "Humpback whale and climate change.csv",
        root / "data" / "raw" / (
            "Movements of Australia's east coast humpback whales.csv"
        ),
        root / "data" / "raw" / (
            "Short-finned pilot whales CRC NW Atlantic.csv"
        ),
        root / "data" / "raw" / (
            "Sperm whales Gulf of California 2007-2008 ADB Tags Argos data.csv"
        ),
        root / "data" / "raw" / (
            "Sperm whales Gulf of Mexico 2011-2013 ADB Tags - Argos data.csv"
        ),
        root / "data" / "raw" / "Whale shark movements in Gulf of Mexico.csv",
    ]
    # Checked with the full data
    assert actual == expected
