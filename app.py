
import os, time, json, math, datetime, urllib.parse, re
from typing import Dict, Any, List
import pandas as pd
import numpy as np
import yfinance as yf
import feedparser
from textblob import TextBlob
from pandas_datareader import data as pdr
from ratelimit import limits, sleep_and_retry
from bs4 import BeautifulSoup
import requests

# -------------------------------
# 0️⃣ Set API keys
# -------------------------------
# 579b464db66ec23bdd000001ca253fa7c51947b1572eb310a731e99d
MY_API_KEY = "579b464db66ec23bdd0000016b699a9bd8da4d0e5653cc18839f110d"  #MCA api key from the Open Government Data Webiste
os.environ["ALPHAVANTAGE_API_KEY"] = "NJSOJQKBF4BHH7Y6"
os.environ["SEC_USER_AGENT"] = "chillakalyan78@gmail.com HackathonApp/1.0"
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
SEC_UA = os.getenv("SEC_USER_AGENT")

# -------------------------------
# 1️⃣ Company metadata
# -------------------------------
COMPANIES = {
    "INFY.NS": {"name": "Infosys", "adr": "INFY", "cin": "L85110KA1981PLC013115"},
    "RELIANCE.NS": {"name": "Reliance Industries", "adr": None, "cin": "L17110MH1973PLC019786"},
    "HDFCBANK.NS": {"name": "HDFC Bank", "adr": "HDB", "cin": "L65920MH1994PLC080618"},
    "TCS.NS": {"name": "Tata Consultancy Services", "adr": None, "cin": "L22210MH1995PLC084781"},
}

# -------------------------------
# 2️⃣ Helper functions
# -------------------------------
def safe_float(x, default=0.0):
    try: return float(x)
    except: return default

def sentiment_of_text(text: str) -> float:
    if not text: return 0.0
    return TextBlob(text).sentiment.polarity

def avg(lst: List[float], default=0.0):
    return sum(lst)/len(lst) if lst else default

# -------------------------------
# 3️⃣ Yahoo Finance
# -------------------------------
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

# -------------------------------
# 4️⃣ FRED + World Bank
# -------------------------------
def get_macro_fred_worldbank(country_code="IND") -> Dict[str, Any]:
    out = {}
    try:
        start = datetime.datetime(2018,1,1)
        end = datetime.datetime.today()
        gdp = pdr.DataReader('GDP', 'fred', start, end)
        out["FRED_GDP"] = safe_float(gdp.iloc[-1].values[0])
    except: out["FRED_GDP"] = 0.0
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

# -------------------------------
# 5️⃣ Alpha Vantage
# -------------------------------
def get_alpha_indicators(symbol="INFY.BSE") -> Dict[str, Any]:
    if not ALPHAVANTAGE_API_KEY:
        return {"ALPHA_used": False, "ALPHA_msg": "No API key set"}
    try:
        url = ("https://www.alphavantage.co/query"
               f"?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey={ALPHAVANTAGE_API_KEY}")
        r = requests.get(url, timeout=20)
        j = r.json()
        ts_key = [k for k in j.keys() if "Time Series" in k]
        if not ts_key: return {"ALPHA_used": True, "ALPHA_vol_30d": 0.0}
        series = j[ts_key[0]]
        closes = [safe_float(vals.get("5. adjusted close", vals.get("4. close", 0))) for d, vals in list(series.items())[:60]]
        closes = list(reversed(closes))
        rets = [math.log(closes[i+1]/closes[i]) for i in range(len(closes)-1) if closes[i]>0 and closes[i+1]>0]
        vol_30d = np.std(rets[-30:]) * math.sqrt(252) if len(rets)>=30 else (np.std(rets)*math.sqrt(252) if rets else 0.0)
        return {"ALPHA_used": True, "ALPHA_vol_30d": vol_30d}
    except: return {"ALPHA_used": True, "ALPHA_vol_30d": 0.0}

# -------------------------------
# 6️⃣ SEC EDGAR filings
# -------------------------------
@sleep_and_retry
@limits(calls=8, period=1)
def _sec_get(url):
    return requests.get(url, headers={"User-Agent": SEC_UA}, timeout=15)

def get_sec_recent_filings(ticker_or_adr: str) -> Dict[str, Any]:
    if not ticker_or_adr: return {"SEC_used": False, "SEC_msg": "No US ticker/ADR"}
    try:
        m = _sec_get("https://www.sec.gov/files/company_tickers.json").json()
        cik = None
        for row in m.values():
            if row.get("ticker","").lower() == ticker_or_adr.lower():
                cik = str(row.get("cik_str")).zfill(10)
                break
        if not cik: return {"SEC_used": False, "SEC_msg": f"CIK not found for {ticker_or_adr}"}
        j = _sec_get(f"https://data.sec.gov/submissions/CIK{cik}.json").json()
        forms = j.get("filings", {}).get("recent", {})
        form_list, dates = list(forms.get("form", [])), list(forms.get("filingDate", []))
        cutoff = datetime.date.today() - datetime.timedelta(days=180)
        recent_count, recent_forms = 0, []
        for f, d in zip(form_list, dates):
            try:
                dt = datetime.datetime.strptime(d, "%Y-%m-%d").date()
                if dt >= cutoff: recent_count+=1; recent_forms.append(f)
            except: pass
        return {"SEC_used": True, "SEC_recent_180d": recent_count, "SEC_recent_forms": recent_forms[:5]}
    except: return {"SEC_used": True, "SEC_recent_180d": 0, "SEC_recent_forms": []}

# -------------------------------
# 7️⃣ MCA data
# -------------------------------
def get_mca_data(cin: str) -> Dict[str, Any]:
    try:
        url = f"https://apisetu.gov.in/api/mca/companies/{cin}"
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            j = res.json()
            return {
                "MCA_used": True,
                "MCA_CompanyName": j.get("companyName"),
                "MCA_Status": j.get("companyStatus"),
                "MCA_Class": j.get("companyClass"),
                "MCA_Category": j.get("companyCategory"),
                "MCA_SubCategory": j.get("companySubCategory"),
                "MCA_PaidUpCapital": j.get("paidUpCapital"),
                "MCA_DateIncorp": j.get("dateOfIncorporation")
            }
        else: return {"MCA_used": False, "MCA_error": f"HTTP {res.status_code}"}
    except: return {"MCA_used": False, "MCA_error": "Request failed"}

# -------------------------------
# 8️⃣ Sector signals
# -------------------------------
def get_sector_signals(company_name: str, ticker_ns: str) -> Dict[str, Any]:
    out = {}
    try:
        stock_price = yf.Ticker(ticker_ns).history(period="1d")["Close"].iloc[-1]
        out["StockPrice"] = float(stock_price)
        if company_name == "Reliance Industries":
            out["BrentOil"] = float(yf.Ticker("BZ=F").history(period="1mo")["Close"].iloc[-1])
            out["ShippingProxyBDRY"] = float(yf.Ticker("BDRY").history(period="1mo")["Close"].iloc[-1])
        elif company_name in ["Infosys", "Tata Consultancy Services"]:
            out["USDINR"] = float(yf.Ticker("INR=X").history(period="1mo")["Close"].iloc[-1])
        elif company_name == "HDFC Bank":
            out["NSEBankIndex"] = float(yf.Ticker("^NSEBANK").history(period="1mo")["Close"].iloc[-1])
    except: pass
    return out

# -------------------------------
# 9️⃣ News & Press Releases
# -------------------------------
def get_news_sentiment(company: str, max_items=10) -> Dict[str, Any]:
    try:
        q = urllib.parse.quote(company)
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={q}")
        titles = [e.title for e in feed.entries[:max_items]]
        sents  = [sentiment_of_text(t) for t in titles]
        return {"News_count": len(titles), "News_sent": avg(sents)}
    except: return {"News_count":0,"News_sent":0.0}

def get_press_release_sentiment(company: str) -> Dict[str, Any]:
    try:
        q = urllib.parse.quote(f'{company} site:{company.split()[0].lower()}.com "press release" OR newsroom OR media')
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={q}")
        titles = [e.title for e in feed.entries[:8]]
        sents  = [sentiment_of_text(t) for t in titles]
        return {"PR_count": len(titles), "PR_sent": avg(sents)}
    except: return {"PR_count":0,"PR_sent":0.0}

def compute_score(data: Dict[str, Any]) -> Dict[str, Any]:
    score = 50  # base score

    # ✅ Financial health
    if data.get("DebtToEquity", 0) < 1: score += 10
    elif data.get("DebtToEquity", 0) > 2: score -= 10

    if data.get("ProfitMargins", 0) > 0.15: score += 10
    else: score -= 5

    # ✅ Sentiment
    score += 5 * data.get("News_sent", 0)
    score += 5 * data.get("PR_sent", 0)

    # ✅ Volatility (AlphaVantage)
    alpha = data.get("AlphaVantage", {})
    if alpha and alpha.get("ALPHA_vol_30d", 0) < 0.2:
        score += 5
    else:
        score -= 5

    # ✅ Bound the score 0–100
    score = max(0, min(100, score))

    return {"Score": score}


# -------------------------------
# 10️⃣ Aggregator (Twitter removed)
# -------------------------------

def fetch_all_sources(ticker_ns: str, meta: Dict[str, Any], api_key: str = MY_API_KEY) -> Dict[str, Any]:
    name, adr = meta["name"], meta.get("adr")
    res: Dict[str, Any] = {"Company": name, "Ticker": ticker_ns}
    res.update(get_financials_yahoo(ticker_ns))
    res.update(get_macro_fred_worldbank("IND"))
    res.update({"AlphaVantage": get_alpha_indicators(symbol=ticker_ns.replace(".NS",""))})
    res.update(get_sec_recent_filings(adr))
    res.update(get_mca_data(meta.get("cin")))
    res.update(get_sector_signals(name, ticker_ns))
    res.update(get_news_sentiment(name))
    res.update(get_press_release_sentiment(name))

    # ⭐ Add scoring here
    res.update(compute_score(res))
    return res

# -------------------------------
# Wrapper functions for clarity
# -------------------------------

# -------------------------------
# 11️⃣ Main Execution with Detailed Output
# -------------------------------
if __name__ == "__main__":
    all_data = []
    results = []

    for ticker, meta in COMPANIES.items():
        print(f"\nFetching data for {meta['name']}...")

        # ✅ Fetch everything
        data = fetch_all_sources(ticker, meta, api_key=MY_API_KEY)
        all_data.append(data)

        # ✅ Build compact scoring summary for CSV
        results.append({
            "Company": meta["name"],
            "Ticker": ticker,
            "Score": data.get("Score", 0),
            "Sentiment": data.get("News_sent", 0.0),
            "DebtToEquity": data.get("DebtToEquity", 0.0),
            "PE_Ratio": data.get("PE_Ratio", 0.0),
            "ProfitMargins": data.get("ProfitMargins", 0.0),
            "SectorData": {k: v for k, v in data.items() if k in ["USDINR","NSEBankIndex","BrentOil","ShippingProxyBDRY","StockPrice"]},
            "PressRelease": data.get("PR_count", 0)
        })

        # ✅ Pretty print details
        print("\n=== Credit Intelligence Platform: Enhanced Prototype ===")
        print(f"Company: {meta['name']} ({ticker})")
        print(f"Financial Data: {{'MarketCap': {data.get('MarketCap')}, 'PE_Ratio': {data.get('PE_Ratio')}, "
              f"'DebtToEquity': {data.get('DebtToEquity')}, 'ProfitMargins': {data.get('ProfitMargins')}}}")
        print(f"Macro Data: {{'FRED_GDP': {data.get('FRED_GDP')}, 'WB_CPI_YoY': {data.get('WB_CPI_YoY')}}}")
        print(f"Sector Data: { {k:v for k,v in data.items() if k in ['USDINR','NSEBankIndex','BrentOil','ShippingProxyBDRY','StockPrice']} }")
        print(f"News Sentiment: {data.get('News_sent',0.0):.2f} (from {data.get('News_count',0)} headlines)")
        print(f"Press Releases: {data.get('PR_count',0)} (avg sent={data.get('PR_sent',0.0):.2f})")
        print(f"SEC Filings (180d): {data.get('SEC_recent_180d','N/A')} forms: {data.get('SEC_recent_forms',[])}")
        print(f"MCA Status: {data.get('MCA_Status','N/A')}, PaidUpCapital: {data.get('MCA_PaidUpCapital','N/A')}")
        print(f"👉 Final Credit Score: {data.get('Score',0):.2f}/100")

    # ✅ Save raw enriched dataset
    df_full = pd.DataFrame(all_data)
    df_full.to_csv("data/all_company_data_MCA.csv", index=False)
    print("\n✅ Saved raw enriched dataset: all_company_data_MCA.csv")

    # ✅ Save scoring summary
    df_scores = pd.DataFrame(results)
    df_scores.to_csv("data/credit_scores_enhanced.csv", index=False)
    print("✅ Saved scoring summary: credit_scores_enhanced.csv")

    # ✅ Quick preview
    print("\n=== Credit Scores ===")
    print(df_scores[["Company","Ticker","Score"]])
    
    
import streamlit as st
import pandas as pd

# ---------------------------------
# Page Setup
# ---------------------------------
st.set_page_config(page_title="Credit Intelligence Dashboard", layout="wide")

# ---------------------------------
# Load Data
# ---------------------------------
@st.cache_data
def load_data():
    try:
        df_full = pd.read_csv("all_company_data_MCA.csv")
        df_scores = pd.read_csv("credit_scores_enhanced.csv")
        df_full.columns = df_full.columns.str.strip()
        df_scores.columns = df_scores.columns.str.strip()
        return df_full, df_scores
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_full, df_scores = load_data()

st.title("📊 Credit Intelligence Platform")
st.write("**Data sources:** Yahoo Finance, Alpha Vantage, SEC EDGAR, MCA (API Setu), World Bank, News & PR sentiment")

if df_full.empty or df_scores.empty:
    st.warning("No data found. Please run the backend script to generate CSV files.")
    st.stop()

# ---------------------------------
# Sidebar - Company Selector
# ---------------------------------
companies = df_scores["Company"].dropna().unique().tolist()
selected_company = st.sidebar.selectbox("🏢 Select a Company", companies)

company_full = df_full[df_full["Company"] == selected_company].iloc[0]
company_score = df_scores[df_scores["Company"] == selected_company].iloc[0]

# ---------------------------------
# Display Key Metrics
# ---------------------------------
st.subheader(f"🏢 {selected_company} — Credit Score: {round(company_score['Score'],2)}/100")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Market Cap", f"{company_full['MarketCap']:,}")
    st.metric("Debt to Equity", round(company_full["DebtToEquity"], 2))
with col2:
    st.metric("P/E Ratio", round(company_full["PE_Ratio"], 2))
    st.metric("Profit Margins", f"{round(company_full['ProfitMargins']*100, 2)}%")
with col3:
    st.metric("News Sentiment", round(company_full.get("News_sent",0), 2))
    st.metric("PR Sentiment", round(company_full.get("PR_sent",0), 2))

# ---------------------------------
# Detailed Data Section
# ---------------------------------
st.markdown("### 📑 Detailed Company Data")
st.dataframe(company_full.to_frame().reset_index().rename(columns={"index":"Field",0:"Value"}))

# ---------------------------------
# Score Comparison Chart
# ---------------------------------
st.markdown("### 📈 Company Score Comparison")
st.bar_chart(df_scores.set_index("Company")["Score"])

# ---------------------------------
# SEC & MCA Info
# ---------------------------------
st.markdown("### 🏛️ Compliance Snapshots")
colA, colB = st.columns(2)
with colA:
    st.write("**SEC Filings (180 days):**")
    st.write(company_full.get("SEC_recent_forms", []))
with colB:
    st.write("**MCA Status:**")
    st.json({
        "Status": company_full.get("MCA_Status","N/A"),
        "PaidUpCapital": company_full.get("MCA_PaidUpCapital","N/A"),
        "Date of Incorporation": company_full.get("MCA_DateIncorp","N/A")
    })

# ---------------------------------
# Footer
# ---------------------------------
st.markdown("---")
st.caption("Built with ❤️ for IIT Kanpur Hackathon — Team Credit Intelligence")
