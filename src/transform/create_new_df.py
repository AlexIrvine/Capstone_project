import logging
import pandas as pd
from src.utils.logging_utils import setup_logger

# Set up the logger with module name and captures every message
logger = setup_logger(__name__, "Create_new_df.log", level=logging.DEBUG)


# Set up the logger with module name and captures every message
def create_combined_df(cleaned_data):

    logger.info("Starting combined df creation")

    # Task 1 - Add a unique identifier for each column
    logger.info("Starting unique column creation")
    cleaned_data = create_unique_column(cleaned_data)
    logger.info("Unique column created")

    # Task 2 - Keep required useful columns
    logger.info("Starting retention of only useful columns")
    cleaned_data = retain_useful_columns(cleaned_data)
    logger.info("Retention of only useful columns done")

    # Task 3 - Keep required useful columns
    logger.info("Starting column_rename")
    cleaned_data = change_column_names(cleaned_data)
    logger.info("Column rename done")

    # Task 4 - Combine all dataframes into one
    logger.info("Starting combining dataframes")
    combined_data = combined_df(cleaned_data)
    logger.info("Combined dataframe done")

    # Return the data
    return combined_data


def create_unique_column(cleaned_data):
    # For every df in the data
    for key, df in cleaned_data.items():
        # Create a new column with study name and tag identifier
        df["study_tag_id"] = (
            df["study-name"].astype(str)
            + "_"
            + df["tag-local-identifier"].astype(str)
        )
        # Save the data
        cleaned_data[key] = df
    return cleaned_data


def retain_useful_columns(cleaned_data):
    # For every df in the data
    for key, df in cleaned_data.items():
        # Save the useful columns for analysis
        df = df[
            [
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
        ]
        # Save the data
        cleaned_data[key] = df
    return cleaned_data


def change_column_names(cleaned_data):
    for key, df in cleaned_data.items():
        df = df.rename(columns={
            "location-lat": "location_lat",
            "location-long": "location_lon",
            "individual-local-identifier": "individual_local_identifier",
            "tag-local-identifier": "tag_local_identifier",
            "individual-taxon-canonical-name":
                "individual_taxon_canonical_name",
            "study-name": "study_name"
        })
        cleaned_data[key] = df
    return cleaned_data


def combined_df(cleaned_data):
    # Set a holder to just store the dfs
    dfs = []
    # For every df in the data save it to the list
    for df in cleaned_data.values():
        dfs.append(df)

    # Combine the dataframes into a combined df
    # Ignore index so no overlaps
    combined_df = pd.concat(dfs, ignore_index=True)
    print(combined_df["individual_taxon_canonical_name"].unique())
    return combined_df
