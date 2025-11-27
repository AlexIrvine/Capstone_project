import pandas as pd


def extract_data() -> pd.DataFrame:  # Test driven development to extract data
    """
    Extract data from a CSV file and return as a DataFrame.
    This function reads data from 'data/source_data.csv'.
    :return: DataFrame containing the extracted data.
    """
    try:
        df = pd.read_csv('data/source_data.csv')
        print("Data extraction successful.")
        return df
    except FileNotFoundError:
        print("Error: The source data file was not found.")
        raise
    except pd.errors.EmptyDataError:
        print("Error: The source data file is empty.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    
    