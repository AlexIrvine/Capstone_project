import subprocess
import sys
from pathlib import Path
import pandas as pd


def test_etl_pipeline_runs_and_creates_output():
    # Project root
    project_root = Path(__file__).resolve().parents[2]

    # Path to script
    run_script = project_root / "scripts" / "run_etl.py"
    assert run_script.exists(), f"run_etl.py not found at {run_script}"

    # Run the etl pipeline
    result = subprocess.run(
        [sys.executable, str(run_script)],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    # The ETL path should succeed
    assert result.returncode == 0, f"ETL pipeline failed: {result.stderr}"

    # Output file
    output_path = (
        project_root
        / "data"
        / "processed"
        / "combined_cleaned_data.csv"
    )
    assert output_path.exists(), "Expected output file not created."

    # File must contain data
    df = pd.read_csv(output_path)
    assert len(df) > 0, "Output CSV is empty."
