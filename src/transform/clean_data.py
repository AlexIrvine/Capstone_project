import logging
import pandas as pd
import geopy.distance
from src.utils.logging_utils import setup_logger

logger = setup_logger(__name__, "Clean_data.log", level=logging.DEBUG)


def clean_data(data_dict):
    logger.info("Starting cleaning dataset")
    # Task 1 - Remove rows with missing longitude or latitude data as they -
    # are useless. 
    logger.info("Starting removing missing values")
    data_dict = remove_missing_values(data_dict)
    logger.info("Missing Values removed")
    # Task 2 - ensure timestamps are in proper datetime.
    logger.info("Starting to ensure timestamp is in datetime")
    data_dict = ensure_datetime(data_dict)
    logger.info("Timestamps in datetime")
    # Task 3 - Calculate distance from previous point
    logger.info("Starting calculation of distance from previous point")
    data_dict = distance_calculator(data_dict)
    # Task 4 - Calculate time from previous point
    logger.info("Starting time delta calculation from previous point")
    data_dict = time_delta(data_dict)
    logger.info("Starting speed calculation")
    data_dict = speed_calculation(data_dict)
    return data_dict


def remove_missing_values(data_dict): 
    try:
        # Missing values are only important in timestamp, latitude, 
        # longitude column
        for key, df in data_dict.items(): 
            data_dict[key] = df.dropna(subset=[
                "timestamp",
                "location-lat",
                "location-long"]
                )
            
        return data_dict
    except Exception as e:
        logger.error(f"Removing missing values failed {e}")
        raise


def ensure_datetime(data_dict):
    try:
        for key, df in data_dict.items():
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            data_dict[key] = df
        return data_dict
    except Exception as e:
        logger.error(f"Conversion to datetime failed {e}")
        raise


def distance_calculator(data_dict):
    try:
        for key, df in data_dict.items(): 
            distances = []
            df = (
                df.sort_values(
                    ["individual-local-identifier", "timestamp"]
                    ).reset_index(drop=True)
            )
            for i in range(len(df)):
                if i == 0:
                    distances.append(0)
                    continue
                same_whale = (
                    df.loc[i, "individual-local-identifier"] 
                    == df.loc[i-1, "individual-local-identifier"]
                )
                if not same_whale: 
                    distances.append(0)
                    continue
                coords_1 = (df.loc[i-1, "location-lat"], df.loc[i-1, "location-long"])
                coords_2 = (df.loc[i, "location-lat"], df.loc[i, "location-long"])
                try:
                    d = geopy.distance.distance(coords_1, coords_2).meters
                except Exception as e:
                    logger.error(f"d = none due to error {e}")
                    d = None
                
                distances.append(d)
            
            df['distance_from_prev_m'] = distances
            data_dict[key] = df
        return data_dict
   
    except Exception as e:
        logger.error(f"Calculation of distance failed {e}")
        raise


def time_delta(data_dict):
    try:
        for key, df in data_dict.items():
            df["time_diff_s"] = (
                df.groupby("individual-local-identifier")["timestamp"]
                .diff()
                .dt.total_seconds()
                )
            
            df['time_diff_s'] = df['time_diff_s'].fillna(0)
            data_dict[key] = df
        return data_dict
    except Exception as e:
        logger.error(f"Calculation of time delta failed {e}")
        raise
        
        
def speed_calculation(data_dict):
    try: 
        for key, df in data_dict.items():
            df['speed_mps'] = df.apply(
                lambda x: x['distance_from_prev_m'] / x['time_diff_s'] 
                if x['time_diff_s'] > 0 else 0,
                axis=1
            )
            data_dict[key] = df
        return data_dict

    except Exception as e:
        logger.error(f"Calculation of mps failed: {e}")
        raise
    
    
def remove_outliers(data_dict):
    try:
        for key, df in data_dict.items():
            data_dict[key] = df[df['speed_mps'] <= 10]
        return data_dict

    except Exception as e:
        logger.error(f"Outlier removal failed: {e}")
        raise
            