# CredTech-Hackathon-Project
CredTech Hackathon Project – Real-time Explainable Credit Intelligence Platform built for IIT Kanpur Hackathon. Ingests multi-source financial + macro + unstructured news data, generates issuer-level credit scores, and provides transparent feature-level explanations via an interactive Streamlit dashboard.



# CredIntel: Explainable Credit Intelligence Platform

### 1. Problem & Objective
This project addresses the **CredTech Hackathon (IIT Kanpur)** challenge: building a real-time, explainable credit intelligence system capable of ingesting heterogeneous structured and unstructured data sources, computing issuer-level scores, and presenting transparent explanations.

### 2. Architecture
- **Ingestion Layer**: Yahoo Finance, Alpha Vantage, SEC EDGAR, FRED, World Bank, Google News/Press Releases.  
- **Feature Engineering**: Normalization, winsorization, financial ratios.  
- **Scoring Engine**: Interpretable rule-based scorecard + optional ML layer with SHAP explainability.  
- **Explainability Layer**: Feature contribution breakdowns, event mappings, short-term vs. long-term indicators.  
- **Presentation**: Streamlit dashboard for analysts.

### 3. Data Sources
- **Structured**: Yahoo Finance, Alpha Vantage, SEC EDGAR, MCA, FRED, World Bank.  
- **Unstructured**: Google News + Press Releases (sentiment analysis via TextBlob + VADER).  
- **Fallbacks**: Defaults and retries for outages.

### 4. Features
- Market cap, PE ratio, debt-to-equity, profit margins.  
- Macroeconomic variables (GDP, inflation, sector indices).  
- Sentiment signals from news/press.  

### 5. Scoring
- Base score with rule-based financial adjustments.  
- Volatility penalties and profitability rewards.  
- Sentiment-driven adjustments.  
- Clamped between 60–90 for stability, with minimum floor for blue-chip issuers.

### 6. Explainability
- Each score linked to feature contributions.  
- SHAP support for tree models.  
- Event-driven text mapping (e.g., debt restructuring → risk increase).  
- No LLM reliance.

### 7. Run Locally
# Clone Repository
git clone https://github.com/chillakalyan/CredTech-Hackathon-Project.git
cd CredTech-Hackathon-Project

# Install required Python packages
pip install -r requirements.txt

# Download TextBlob corpora for sentiment analysis
python -m textblob.download_corpora

# Launch the Streamlit dashboard
streamlit run src/app.py

### 8. Docker
pending 

### 9. Testing
pending

### 10. Trade-offs & Alternatives
pending

### 11.Roadmap


## 📂 Repo Structure

```bash
cred-intel/
├── src/
│   ├── ingest/
│   │   ├── yfin.py              # Yahoo Finance fetch
│   │   ├── fred.py              # Macro data (FRED + World Bank)
│   │   ├── rss.py               # News + sentiment + event tags
│   ├── features/
│   │   └── build_features.py    # Normalization, winsorize, joins
│   ├── model/
│   │   ├── scorecard.py         # Interpretable scoring
│   │   ├── tree_model.py        # Optional decision tree + SHAP utils
│   │   └── explain.py           # SHAP + event deltas → text
│   ├── utils/
│   │   ├── cache.py             # Last good value, staleness
│   │   ├── retry.py             # Retry/backoff
│   │   └── config.py            # API keys, refresh interval
│   ├── app.py                   # Streamlit dashboard (main entry)
│   └── pipeline.py              # Fetch-all-sources aggregator
│
├── data/
│   ├── snapshots/               # Parquet snapshots by timestamp
│   └── demo.csv                 # Small demo to run offline
│
├── tests/
│   ├── test_ingest.py
│   ├── test_features.py
│   └── test_scorecard.py
│
├── Dockerfile                   # Container spec
├── requirements.txt             # Dependencies
├── README.md                    # Documentation
├── PRESENTATION.pdf             # Submission deck
└── run.sh                       # Helper script (docker run)


