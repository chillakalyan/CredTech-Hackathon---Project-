import pytest
import pandas as pd

def test_score_range():
    df = pd.read_csv("credit_scores.csv")
    for score in df["Score"]:
        assert 0 <= score <= 100, f"Score {score} out of range (0–100)"

def test_company_names_exist():
    df = pd.read_csv("credit_scores.csv")
    assert df["Company"].notnull().all(), "All companies should have names"

