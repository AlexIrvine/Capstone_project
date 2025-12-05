import logging
import pandas as pd
import geopy.distance
from src.utils.logging_utils import setup_logger


# Set up the logger with module name and captures every message
logger = setup_logger(__name__, "Clean_data.log", level=logging.DEBUG)


def clean_data(data_dict):
    logger.info("Starting cleaning dataset")

    # Task 1 - Remove rows with missing longitude or latitude data
    logger.info("Starting removing missing values")
    data_dict = remove_missing_values(data_dict)
    logger.info("Missing Values removed")

    # Task2 - Drop duplicates 
    logger.info("Starting duplicate removal")
    data_dict = drop_duplicates(data_dict)

    # Task 3 - ensure timestamps are in proper datetime format
    logger.info("Starting to ensure timestamp is in datetime")
    data_dict = ensure_datetime(data_dict)
    logger.info("Timestamps in datetime")

    # Task 4 - Calculate distance from previous point
    logger.info("Starting calculation of distance from previous point")
    data_dict = distance_calculator(data_dict)

    # Task 5 - Calculate time deltas from previous point
    logger.info("Starting time delta calculation from previous point")
    data_dict = time_delta(data_dict)

    # Task 6 - Remove time deltas of zero
    logger.info("Starting removal of time delta")
    data_dict = remove_zero_time_delta(data_dict)

    # Task 7 - Calculate speed from previous point
    logger.info("Starting speed calculation")
    data_dict = speed_calculation(data_dict)

    # Task 8 - Remove Outliers
    logger.info("Starting outlier removal")
    data_dict = remove_outliers(data_dict)

    # Task 9 - Re-run calculations after outlier removal
    logger.info("Starting calculation of distance from previous point - 2")
    data_dict = distance_calculator(data_dict)

    logger.info("Starting time delta calculation from previous point - 2")
    data_dict = time_delta(data_dict)

    logger.info("Starting removal of time delta - 2")
    data_dict = remove_zero_time_delta(data_dict)

    logger.info("Starting speed calculation - 2")
    data_dict = speed_calculation(data_dict)

    # Task 10 fill in missing
    logger.info("Filling in missing taxon name")
    data_dict = fill_missing_column(data_dict)

    data_dict = change_species_names(data_dict)
    return data_dict


def remove_missing_values(data_dict):
    try:
        """
        Missing values important in timestamp, lat, long, IDs, tag
        For each df drop these rows if NAs are present
        """
        for key, df in data_dict.items():
            data_dict[key] = df.dropna(
                subset=[
                    "timestamp",
                    "location-lat",
                    "location-long",
                    "individual-local-identifier",
                    "tag-local-identifier",
                ]
            )
        return data_dict

    except Exception as e:
        logger.error(f"Removing missing values failed {e}")
        raise


def drop_duplicates(data_dict):
    # Drop duplicates
    try:
        before = 0
        after = 0
        dropped = 0
        for key, df in data_dict.items():
            before += len(df)
            df = df.drop_duplicates()
            after = +len(df)
            dropped += before - after
            # Resent index to avoid issues in distance calc
            data_dict[key] = df.reset_index(drop=True)

        logger.info(
                f"[{key}] Duplicate rows removed: {dropped} "
                f"(before: {before}, after: {after})"
            )
        return data_dict

    except Exception as e:
        logger.error(f"Duplicate removal failed: {e}")
        raise


def ensure_datetime(data_dict):
    try:
        nas = 0
        # Ensure the timestamp column is in correct format
        for key, df in data_dict.items():
            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                format="mixed",
                errors="coerce")
            data_dict[key] = df
            # Add nas from each data set
            nas += df["timestamp"].isna().sum()

        logger.info(f"{nas} NAs across all timestamp")
        return data_dict
    except Exception as e:
        logger.error(f"Conversion to datetime failed {e}")
        raise


def distance_calculator(data_dict):
    try:
        # For every df
        for key, df in data_dict.items():
            # Set up a store for distances
            distances = []
            # Sort the rows so the distance calculation is correct
            df = (
                # Sorted so individual , then tag then timestamp
                # Index resent so indexing loc works
                df.sort_values(
                    [
                        "individual-local-identifier",
                        "tag-local-identifier",
                        "timestamp"
                        ]
                ).reset_index(drop=True)
            )

            # Iterate i for the entire dataset
            for i in range(len(df)):
                # If i is 0 (the first row) should be zero (no previous)
                if i == 0:
                    distances.append(0)
                    continue
                # Same whale true if previous Whale-ID and Tag-ID equal
                same_whale = (
                    df.loc[i, "individual-local-identifier"]
                    == df.loc[i - 1, "individual-local-identifier"]
                    and df.loc[i, "tag-local-identifier"]
                    == df.loc[i - 1, "tag-local-identifier"]
                )
                # If it is not true it must be a new whale or tag
                if not same_whale:
                    # Every new whale and tag should be zero
                    distances.append(0)
                    continue

                # If same whale was true retrieve coords
                coords_1 = (
                    df.loc[i - 1, "location-lat"],
                    df.loc[i - 1, "location-long"],
                )
                coords_2 = (
                    df.loc[i, "location-lat"],
                    df.loc[i, "location-long"],
                )

                try:
                    # use geopy to calculate distance
                    d = geopy.distance.distance(coords_1, coords_2).meters
                except Exception as e:
                    logger.error(f"d = None due to error {e}")
                    d = None
                # Add it to distances
                distances.append(d)

            # Add a new column with the data from distances
            df["distance_from_prev_m"] = distances
            # Save this back to the key
            data_dict[key] = df

        return data_dict

    except Exception as e:
        logger.error(f"Calculation of distance failed {e}")
        raise


def time_delta(data_dict):
    try:
        for key, df in data_dict.items():
            # Create a time delta column
            # Calculate delta grouped by Whale-ID an Tag-ID
            # Save the difference as seconds
            df["time_diff_s"] = (
                df.groupby(
                    ["individual-local-identifier", "tag-local-identifier"]
                )["timestamp"]
                .diff()
                .dt.total_seconds()
            )

            # Nas left over from calculation filled with 0
            df["time_diff_s"] = df["time_diff_s"].fillna(0)
            # Save it back
            data_dict[key] = df

        return data_dict

    except Exception as e:
        logger.error(f"Calculation of time delta failed {e}")
        raise


def remove_zero_time_delta(data_dict):
    try:
        for key, df in data_dict.items():
            # Set up a store
            valid_rows = []

            # For i in the length of the df
            for i in range(len(df)):

                # If i zero a zero time delta allowed
                if i == 0:
                    valid_rows.append(i)
                    continue

                # Set up same whale logic again
                same_whale = (
                    df.loc[i, "individual-local-identifier"]
                    == df.loc[i - 1, "individual-local-identifier"]
                    and df.loc[i, "tag-local-identifier"]
                    == df.loc[i - 1, "tag-local-identifier"]
                )

                # If it is not the same whale or tag a zero delta is valid
                if not same_whale:
                    valid_rows.append(i)
                    continue

                # All other rows above 0 valid
                if df.loc[i, "time_diff_s"] > 0:
                    valid_rows.append(i)
            # Only keep rows with ame index as valid rows and removes old index
            data_dict[key] = df.loc[valid_rows].reset_index(drop=True)

        return data_dict

    except Exception as e:
        logger.error(f"Removal of time delta failed {e}")
        raise


def speed_calculation(data_dict):
    try:
        for key, df in data_dict.items():
            # Apply a speed calculation to the df creating a new column
            # Need else 0 to account for new whales etc
            # Axis = 1 row by row calc
            df["speed_mps"] = df.apply(
                lambda x: (
                    x["distance_from_prev_m"] / x["time_diff_s"]
                    if x["time_diff_s"] > 0
                    else 0
                ),
                axis=1,
            )
            # Save it back to dictionary
            data_dict[key] = df

            # Define too fast recordings as those exceeding 10 m/s
            # Too fast based on blue whales future use expand this
            too_fast = (df["speed_mps"] > 10).sum()
            print(f"Number of too fast recordings: {too_fast}")

        return data_dict

    except Exception as e:
        logger.error(f"Calculation of mps failed: {e}")
        raise


def remove_outliers(data_dict):
    try:
        for key, df in data_dict.items():
            # Save original length of df
            original = len(df)
            # Filter on speed
            filtered = df[df["speed_mps"] <= 10]
            # Save filtered length
            after = len(filtered)

            # calculate and declare a percentage to evaluate removal
            percent = (after / original) * 100
            print(f"Percentage of rows remaining {percent}")

            data_dict[key] = filtered

        return data_dict

    except Exception as e:
        logger.error(f"Outlier removal failed: {e}")
        raise


# Issue found through testing no taxon name in Narwhal data
def fill_missing_column(data_dict):
    # Manually fill in this data set
    # Future work try and make this automatic?
    key = (
        "Baffin Bay narwhal- 2009 to 2012 Argos data- "
        "Fisheries and Oceans Canada"
        )

    if key in data_dict:
        df = data_dict[key]

        df["individual-taxon-canonical-name"] = df[
            "individual-taxon-canonical-name"
        ].fillna("Narwhal")

        data_dict[key] = df

    return data_dict


def change_species_names(data_dict):
    mapping = {
        "Balaenoptera musculus": "Blue whale",
        "Balaenoptera physalus": "Fin whale",
        "Balaenoptera borealis": "Sei whale",
        "Narwhal": "Narwhal",
        "Monodon monoceros": "Narwhal",
        "Balaenoptera": "Balaenopterid whale (unspecified)",
        "Balaena mysticetus": "Bowhead whale",
        "Pseudorca crassidens": "False killer whale",
        "Megaptera novaeangliae": "Humpback whale",
        "Globicephala macrorhynchus": "Short-finned pilot whale",
        "Globicephala": "Pilot whale (unspecified)",
        "Physeter macrocephalus": "Sperm whale",
        "Rhincodon typus": "Whale shark",
    }

    for key, df in data_dict.items():
        if "individual-taxon-canonical-name" in df.columns:
            df["individual-taxon-canonical-name"] = (
                df["individual-taxon-canonical-name"].replace(mapping)
            )
            data_dict[key] = df

    return data_dict
# Future work re-order work flow to improve efficiency
