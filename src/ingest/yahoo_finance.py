import yfinance as yf
from typing import Dict, Any

def get_financials_yahoo(ticker_ns: str) -> Dict[str, Any]:
    try:
        stock = yf.Ticker(ticker_ns)
        info = stock.info or {}
        return {
            "Ticker": ticker_ns,
            "MarketCap": info.get("marketCap", 0),
            "PE_Ratio": info.get("trailingPE", 0),
            "DebtToEquity": info.get("debtToEquity", 0),
            "ProfitMargins": info.get("profitMargins", 0)
        }
    except:
        return {"Ticker": ticker_ns, "MarketCap": 0, "PE_Ratio": 0, "DebtToEquity": 0, "ProfitMargins": 0}
