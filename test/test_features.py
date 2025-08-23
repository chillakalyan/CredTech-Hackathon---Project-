import pytest
import pandas as pd
from src.pipeline import fetch_all_sources, COMPANIES

def test_fetch_all_sources_returns_dict():
    ticker, meta = list(COMPANIES.items())[0]  # pick first company
    result = fetch_all_sources(ticker, meta)
    assert isinstance(result, dict), "fetch_all_sources should return a dictionary"
    assert "Company" in result
    assert "Score" in result

