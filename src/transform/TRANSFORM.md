# User Story 3: Clean, Standardise Data

**As a data engineer**,  
I want to clean and standardise raw whale data,  
so that invalid, inconsistent, or biologically impossible data points do not affect downstream analysis.

### Cleaning Requirements
- Remove rows missing required fields:  
  `timestamp`, `location-lat`, `location-long`,  
  `individual-local-identifier`, `tag-local-identifier`.
- Drop all duplicate rows and store amount
- Convert all timestamps using `pd.to_datetime` with coercion and count NAs.
- Sort data by:  
  `individual-local-identifier` -> `tag-local-identifier` -> `timestamp`.
- Remove invalid zero-time-delta rows for the same whale + tag (except group starts).
- Fill missing species names for affected studies (e.g., Narwhal dataset).

### Movement Metric Requirements
- Calculate distance (`distance_from_prev_m`) using GeoPy.
- Compute time deltas (`time_diff_s`) grouped by whale + tag.
- Compute speed (`speed_mps`) ensuring:
  - speed = 0 when `time_diff_s == 0`  
  - No negative or Na speeds  
- Remove biologically impossible speeds (`speed_mps > 10`).
- Recalculate distance, time-delta, and speed after removing outliers.

---

## Definition of Done
- Cleaned DataFrames contain no invalid timestamps, no missing required fields, and correct chronological ordering.
- Movement metrics (`distance_from_prev_m`, `time_diff_s`, `speed_mps`) are present and valid.
- Zero-delta rows removed appropriately.
- Outlier speeds (>10 m/s) removed (partially), and metrics recalculated.
- All cleaning tests pass.

---

## Testing Strategy (Clean Stage)

Unit tests validate:

- **Missing value removal:**  
  - Removes rows with missing required fields  
  - Retains correct rows  
  - Ensures no NAs remain in required columns  

- **Timestamp standardisation:**  
  - Checks the function is callable  
  - Verifies all timestamps become datetime objects  
  - Confirms invalid strings convert to NA  
  - Tests behaviour on real Movebank data  

- **Distance calculation correctness:**  
  - First calculated distance is always zero  
  - GeoPy distance matches expected value  
  - Sorting logic works correctly  
  - Distance resets to zero for each new whale and tag  
  - All distances are positive  
  - Distance column length equals DataFrame length  

- **Time delta logic:**  
  - Time difference is calculated correctly  
  - First value for each whale-tag group is zero  
  - New whale/tag correctly resets time delta to zero  
  - After zero-time-delta removal, no unwanted zeros remain for same whale and tag  

- **Speed calculation logic:**  
  - Speed is zero when time delta is zero  
  - Speed column length matches DataFrame  
  - No negative speeds  
  - No Na speeds  

- **Outlier removal:**  
  - Tested on fake data (real data unsuitable)  
  - Ensures rows above 10 m/s are removed  

- **Final validation checks:**  
  - All required metric columns exist  
  - No missing timestamps remain  

## Future work
- **A lot**
- Removing Zero time deltas is good as they do not help with progression. However, the distances may be different: 
  - An outlier may be kept in when a good one is thrown out if their is two recording at the same time.
- Entire logical flow could be better e.g. removing NAs after time ensuring time calculation. 
- Outlier removal algorithm needs to be more sophisticated:
  - Back-to-back outliers may escape removal  
  - Could check neighbouring rows when identifying outliers  
  - Using a statistical test to class the outer limits was considered but was avoided as with real data a whale may move miles after staying in one place. 
  - 10 m/s is based of blue whales. Did not have time to create a dictionary of each whales maximal speed. 
  - Check angles of movement. 
  - A speed curve over time to enforce what is physically possible. 

## Problems faced
- I needed to sort prior to calculation otherwise the shifting did not work. 
- Realised I needed to also sort by tag-id in case one whale had multiple tags. 
- Index was not reset early on, breaking `iloc`-based calculations. 
- Removing outliers rows created gaps that required recalculating distances, which still left some outliers.
- Afformentioned issues with outlier removal 
- The Narwhal dataset had no species identifier, this had to be manually inserted.
- Realised more whales did not have species identifiers but did not have time to code it in.


# User Story 4: Combine and Standardise 

**As a data engineer**,  
I want to standardise column names, retain only meaningful analytical columns, and combine all cleaned GPS into a single dataset, so that downstream visualisations and analysis operate on a unified, consistent schema.

---

## Acceptance Criteria

### Schema Standardisation
- Add a unique `study_tag_id` column using:  
  `study-name` + `_` + `tag-local-identifier`.
- Retain only analytically useful columns:
  - `study_tag_id`
  - `timestamp`
  - `location-lat`
  - `location-long`
  - `distance_from_prev_m`
  - `time_diff_s`
  - `speed_mps`
  - `individual-local-identifier`
  - `tag-local-identifier`
  - `individual-taxon-canonical-name`
  - `study-name`
- Rename fields to a consistent snake_case schema:
  - `location-lat` → `location_lat`  
  - `location-long` → `location_lon`  
  - `individual-local-identifier` → `individual_local_identifier`  
  - `tag-local-identifier` → `tag_local_identifier`  
  - `individual-taxon-canonical-name` → `individual_taxon_canonical_name`  
  - `study-name` → `study_name`

### Combination Requirements
- Combine all cleaned DataFrames into a single unified DataFrame.
- Final dataset must contain no missing values in required analytical fields.
- Combined dataset length must equal the sum of all input frames.

---

## Definition of Done
- All data from all studies combined into a single DataFrame.
- All required columns present and correctly renamed.
- Combined dataset contains no missing required analytical values.
- All tests pass.

---

## Testing Strategy (Combine Stage)

Unit tests validate:

- **study_tag_id creation:**  
  - No NAs in required columns 
  - All values are strings  

- **Column retention:**  
  - Correct set of analytical columns preserved  
  - No missing values in retained columns  

- **Column renaming:**  
  - All expected names present  
  - No old names remain  

- **Structure:**  
  - Final output is a pandas DataFrame  
  - Expected number of columns is present 
  
# Final coverage was 
- 84% for cleaning data 
- 100% for creating a new dataframe

## Future work 

- Improve readability of `study_tag_id`.
- Consider species + a unique index for more meaningful identifiers.
- Perform more testing on data types in columns

## Issues faced

- Streamlit components required `_` instead of `-`, forcing column renaming.
- Some columns had Nas such as some species but could not hard code them all.

Component tests validate:

- `clean_data()` produces a dict of cleaned DataFrames with required columns  
- No missing timestamps remain  
- Sorting and grouping behaviour is correct  
- `create_combined_df()` returns a single DataFrame
- Combined dataset length equals sum of all cleaned DataFrames
- All required analytical columns present in final dataset
- Correct length   

## Takeaways
- Its not good enough to just plan the project, you have to think about all the logical steps and how they will flow onto each other. Next time I do a project like this I will leave a day for refactoring the code.
- Include big O complexity in requirements