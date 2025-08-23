"""
prototype.py
Offline runner that uses pipeline.py to fetch + save company data
"""

import pandas as pd
from pipeline import COMPANIES, fetch_all_sources

if __name__ == "__main__":
    all_data, results = [], []

    for ticker, meta in COMPANIES.items():
        print(f"\nFetching data for {meta['name']}...")
        data = fetch_all_sources(ticker, meta)
        all_data.append(data)

        results.append({
            "Company": meta["name"],
            "Ticker": ticker,
            "Score": data.get("Score", 0),
            "Sentiment": data.get("News_sent", 0.0),
            "DebtToEquity": data.get("DebtToEquity", 0.0),
            "PE_Ratio": data.get("PE_Ratio", 0.0),
            "ProfitMargins": data.get("ProfitMargins", 0.0),
            "SectorData": {k: v for k, v in data.items()
                           if k in ["USDINR","NSEBankIndex","BrentOil","ShippingProxyBDRY","StockPrice"]},
            "PressRelease": data.get("PR_count", 0)
        })

        print(f"👉 Final Credit Score for {meta['name']}: {data.get('Score',0)}/100")

    # ✅ Save datasets
    df_full = pd.DataFrame(all_data)
    df_full.to_csv("all_company_data_MCA.csv", index=False)
    print("\n✅ Saved: all_company_data_MCA.csv")

    df_scores = pd.DataFrame(results)
    df_scores.to_csv("credit_scores_enhanced.csv", index=False)
    print("✅ Saved: credit_scores_enhanced.csv")

    print("\n=== Credit Scores ===")
    print(df_scores[["Company","Ticker","Score"]])
