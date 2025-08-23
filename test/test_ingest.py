import pytest
import os
import pandas as pd

def test_ingest_output_files_exist():
    # Run the pipeline script before running this test
    assert os.path.exists("data/all_company_data.csv"), "all_company_data.csv should be generated"
    assert os.path.exists("data/credit_scores.csv"), "credit_scores.csv should be generated"

def test_ingest_csv_validity():
    df = pd.read_csv("credit_scores.csv")
    assert "Company" in df.columns
    assert "Score" in df.columns
    assert not df.empty, "credit_scores.csv should not be empty"

