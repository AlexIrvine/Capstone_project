# User Story 5: Load Transformed Dataset

**As a data analyst or Streamlit user**,  
I want the final combined dataset saved to a consistent location,  
so that the Streamlit app can reliably read it.

## Acceptance Criteria

- Create the `data/processed` directory
- Save the file without an index
- The function returns the full path to the saved file.

## Definition of Done
- CSV exists at the correct path.
- Row count matches the input DataFrame.
- No index column in the saved CSV.

## Testing Strategy
A single unit test checks that:
- The file is created.
- The returned path exists.
- Reloading the CSV reproduces the correct number of rows.

---
## Coverage 
- 100%

## Issues / Future Work
- Add checks before saving.
- Improve error handling for invalid inputs.