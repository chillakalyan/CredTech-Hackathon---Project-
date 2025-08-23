import os, math, numpy as np, requests
from typing import Dict, Any

# ✅ Force set API key (temporary, for local/dev use)
os.environ["ALPHAVANTAGE_API_KEY"] = "NJSOJQKBF4BHH7Y6"
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def safe_float(x, default=0.0):
    try: return float(x)
    except: return default

def get_alpha_indicators(symbol="INFY.BSE") -> Dict[str, Any]:
    if not ALPHAVANTAGE_API_KEY:
        return {"ALPHA_used": False, "ALPHA_msg": "No API key set"}
    try:
        url = ("https://www.alphavantage.co/query"
               f"?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey={ALPHAVANTAGE_API_KEY}")
        r = requests.get(url, timeout=20)
        j = r.json()
        ts_key = [k for k in j.keys() if "Time Series" in k]
        if not ts_key: 
            return {"ALPHA_used": True, "ALPHA_vol_30d": 0.0}
        
        series = j[ts_key[0]]
        closes = [safe_float(vals.get("5. adjusted close", vals.get("4. close", 0))) 
                  for d, vals in list(series.items())[:60]]
        closes = list(reversed(closes))
        
        rets = [math.log(closes[i+1]/closes[i]) for i in range(len(closes)-1) 
                if closes[i]>0 and closes[i+1]>0]
        
        vol_30d = np.std(rets[-30:]) * math.sqrt(252) if len(rets)>=30 else (
                  np.std(rets)*math.sqrt(252) if rets else 0.0)
        
        return {"ALPHA_used": True, "ALPHA_vol_30d": vol_30d}
    except:
        return {"ALPHA_used": True, "ALPHA_vol_30d": 0.0}

