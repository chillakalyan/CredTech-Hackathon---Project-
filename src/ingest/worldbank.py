import requests
from typing import Dict, Any

def safe_float(x, default=0.0):
    try: return float(x)
    except: return default

def get_macro_worldbank(country_code="IND") -> Dict[str, Any]:
    out = {}
    try:
        wb_url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/FP.CPI.TOTL.ZG?format=json&per_page=5"
        r = requests.get(wb_url, timeout=15)
        data = r.json()
        val = None
        if isinstance(data, list) and len(data) == 2:
            for row in data[1]:
                if row.get("value") is not None:
                    val = row["value"]; break
        out["WB_CPI_YoY"] = safe_float(val, 0.0)
    except: out["WB_CPI_YoY"] = 0.0
    return out

