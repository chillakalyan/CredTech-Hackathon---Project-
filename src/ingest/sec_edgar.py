import os, requests, datetime
from ratelimit import limits, sleep_and_retry
from typing import Dict, Any

# ✅ Force set User-Agent for SEC API (temporary, for dev use)
os.environ["SEC_USER_AGENT"] = "chillakalyan78@gmail.com HackathonApp/1.0"
SEC_UA = os.getenv("SEC_USER_AGENT")

# ✅ Rate limit (SEC allows ~10 requests/sec, we stay safe at 8)
@sleep_and_retry
@limits(calls=8, period=1)
def _sec_get(url):
    return requests.get(url, headers={"User-Agent": SEC_UA}, timeout=15)

def get_sec_recent_filings(ticker_or_adr: str) -> Dict[str, Any]:
    """
    Fetches last 180 days filings from SEC for a given ticker/ADR.
    """
    if not ticker_or_adr:
        return {"SEC_used": False, "SEC_msg": "No US ticker/ADR provided"}

    try:
        # Step 1: Get full ticker → CIK mapping
        m = _sec_get("https://www.sec.gov/files/company_tickers.json").json()

        cik = None
        for row in m.values():
            if row.get("ticker", "").lower() == ticker_or_adr.lower():
                cik = str(row.get("cik_str")).zfill(10)
                break

        if not cik:
            return {"SEC_used": False, "SEC_msg": f"CIK not found for {ticker_or_adr}"}

        # Step 2: Get filings for that CIK
        j = _sec_get(f"https://data.sec.gov/submissions/CIK{cik}.json").json()
        forms = j.get("filings", {}).get("recent", {})
        form_list, dates = list(forms.get("form", [])), list(forms.get("filingDate", []))

        # Step 3: Keep only last 180 days
        cutoff = datetime.date.today() - datetime.timedelta(days=180)
        recent_forms = [
            f for f, d in zip(form_list, dates)
            if d and datetime.datetime.strptime(d, "%Y-%m-%d").date() >= cutoff
        ]

        return {
            "SEC_used": True,
            "SEC_recent_180d": len(recent_forms),
            "SEC_recent_forms": recent_forms[:5]
        }
    except:
        return {"SEC_used": True, "SEC_recent_180d": 0, "SEC_recent_forms": []}
