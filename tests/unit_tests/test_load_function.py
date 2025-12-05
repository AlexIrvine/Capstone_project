import pandas as pd
from src.load.load import save_combined_csv


def test_save_combined_csv_saves_file():
    df = pd.DataFrame({"col": [1, 2, 3]})

    # Call the function
    result_path = save_combined_csv(df)

    # Assert the function returned a Path
    assert result_path.exists()

    # Assert the file contains something
    loaded = pd.read_csv(result_path)
    assert len(loaded) == 3
