# User Story 2: Extract Raw GPS Data

**As a data engineer**,  
I want to extract multiple raw CSV files from Movebank studies into a structured format,  
so that all whale GPS data is available in a consistent format for Transform.

### Acceptance Criteria

- All CSV files in `data/raw/` load successfully.  
- Files are read into DataFrames with standardised names.  
- Logs record:
  - file name  
  - file path  
  - row count    
- Extraction fails if:
  - a file cannot be opened  
  - the directory does not exist  

---

### Definition of Done

- All CSVs load without errors in a normal run.  
- Extraction returns a dictionary mapping study names to DataFrames.    
- Issues or missing files appear in logs.  
- Unit and integration extraction tests pass successfully.

---

### Testing Strategy

Testing for this story aimed to verify if file path discovery and file loading behaviours worked.

Two main components were tested:

1. **File list creation**  
2. **DataFrame extraction into memory**

## Unit tests
#### 1. File Extraction Tests  
(`test_file_extraction.py`)

These tests validate:

- The `data/raw` directory is correctly resolved.
- Only valid `.csv` files are included (ignoring poor file names or non-CSV files).
- The list of files returned matches the expected full dataset.

Example behaviours tested:
- Directory path correctness.
- Filtering of CSV vs non-CSV.  
- Correct file ordering.

#### 2. DataFrame Loading Tests  
(`test_data_dict_creation.py`)

These tests validate:

- The extraction function returns a dictionary.  
- Each value is a non-empty DataFrame.  
- Keys match expected cleaned study names.  
- The number of DataFrames equals the number of test files.
  
## Component tests

This test validates: 
- The full function works combines.
- Ensures the return is not empty.
- Is a dictionary.
- File naming convention is correct and present.
- All values are dataframes and not empty. 
### Coverage: 

- Create File List 78%
- Extract Files into Df 83%
- Extract Component 79%


| Data set                                                                                            | Rows   |
|-----------------------------------------------------------------------------------------------------|--------|
| Loaded Antarctic blue whales, east Antarctic sector of the Southern Ocean                           | 835    |
| Loaded Azores Great Whales Satellite Telemetry Program                                              | 7006   |
| Loaded Baffin Bay narwhal 2009 to 2012 Argos data                                                   | 48398  |
| Loaded Blue and fin whales Southern California 2014–2015 Argos data                                 | 4303   |
| Loaded Blue and fin whales Southern California 2014–2015 Fastloc GPS data                           | 17169  |
| Loaded Blue whales Eastern North Pacific 1993–2008 Argos data                                       | 16106  |
| Loaded Blue whales Eastern North Pacific 2003 State-space model output                              | 149    |
| Loaded Bowhead whale Admiralty Inlet                                                                | 675    |
| Loaded Bowhead whale Cumberland Sound                                                               | 41404  |
| Loaded Bowhead whale Foxe Basin                                                                     | 50235  |
| Loaded False Killer Whales – Hawaiian Islands                                                       | 5155   |
| Loaded Fin whales Gulf of California 2001 – Argos data                                              | 572    |
| Loaded Humpback whale and climate change                                                            | 702    |
| Loaded Movements of Australia's east coast humpback whales                                          | 30388  |
| Loaded Short-finned pilot whales CRC NW Atlantic                                                    | 33141  |
| Loaded Sperm whales Gulf of California 2007–2008 ADB Tags                                           | 1261   |
| Loaded Sperm whales Gulf of Mexico 2011–2013 ADB Tags                                               | 5638   |
| Loaded Whale shark movements in Gulf of Mexico                                                      | 3424   |

### Future Improvements

- Add validation to ensure required columns exist before.
- Remove hard coding within tests ran out of time to change it. 
- Add logging of file sizes and memory.  
- Add speed test of extraction.
- Be able to handle FastLoc data in the same function.
- Test error handling which are causing lower coverage.
- Better naming convention(This will be a theme)

---

## Takeaways
- Tests should definitely not be hardcoded but I was struggling with the mock tests. 
- I liked how my data read in as it kept consistent names with the data.