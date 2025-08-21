# fred.py
# Macro data (FRED + World Bank)

import pandas_datareader.data as web
import pandas as pd
from datetime import datetime

def fetch_fred_data(series_id: str, start="2015-01-01"):
    """
    Fetch macroeconomic series from FRED.
    """
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        df = web.DataReader(series_id, "fred", start_date)
        return df
    except Exception as e:
        print(f"Error fetching {series_id}: {e}")
        return pd.DataFrame()

