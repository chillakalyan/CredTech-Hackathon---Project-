# 🚀 CredTech – AI-powered Credit Intelligence Platform  

[![View Dashboard](https://img.shields.io/badge/Live-Dashboard-brightgreen?style=for-the-badge&logo=streamlit)](https://credtech-hackathon-project-xdokbheb2scyyendh4cq7v.streamlit.app/)

👉 **Live Demo**: [Click here to open the Streamlit App](https://credtech-hackathon-project-xdokbheb2scyyendh4cq7v.streamlit.app/)


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
We use a Dockerfile to containerize the entire project for portability and reproducibility. The image bundles all dependencies (`Python`, `pandas`, `numpy`, `yfinance`, `scikit-learn`, `streamlit`, etc.) and exposes the Streamlit app. This ensures that the project can run seamlessly across different environments, including local machines, cloud VMs, and hackathon submission servers.

Key points:
- `Dockerfile` defines the base image (Python 3.10+) and dependencies.
- `run.sh` is provided as a helper script to build and run the container.
- Supports deployment on Streamlit Cloud, Docker Hub, or any container orchestration system (Kubernetes, AWS ECS, etc.).

### 9. Testing
The `tests/` folder contains unit tests to validate data ingestion, feature engineering, and the scoring logic:
- `test_ingest.py` → Ensures all APIs (Yahoo Finance, Alpha Vantage, SEC, World Bank, News) return expected schemas.
- `test_features.py` → Validates transformations like normalization, winsorization, and joins.
- `test_scorecard.py` → Tests the scoring engine with synthetic and real company data.

Tests are executed using `pytest`. This makes the system more reliable and ensures quick debugging during hackathons or deployments.

### 10. Trade-offs & Alternatives
- **Data Sources**: We focused on free/public APIs (Yahoo Finance, Alpha Vantage, World Bank, SEC, MCA via API Setu). Paid APIs (e.g., Bloomberg, Refinitiv) provide more depth but were avoided due to cost.
- **Modeling Approach**: Chose interpretable scorecards instead of complex deep learning for transparency. However, a tree-based model (XGBoost/LightGBM with SHAP explainability) is available for experimentation.
- **Deployment**: Streamlit Cloud chosen for simplicity and hackathon-readiness. Alternatives include AWS, GCP, or Azure with CI/CD pipelines.
- **Scoring**: Balanced between quantitative (financial ratios, volatility) and qualitative (sentiment, compliance). Could extend with graph-based risk networks.

### 11. Roadmap
- **Short-term (Hackathon-ready)**
  - Polish Streamlit dashboard (comparison charts, compliance summaries).
  - Improve sentiment analysis with pretrained NLP models (e.g., FinBERT).
  - Add caching + retry logic for API robustness.

- **Mid-term (Pilot with Banks/Fintechs)**
  - Expand to 50–100 companies across multiple sectors.
  - Add alerting system for credit score changes.
  - Provide CSV/Excel export and API endpoints for integration.

- **Long-term (Production-Scale)**
  - Integrate premium data providers (Bloomberg, Refinitiv) for high accuracy.
  - Enable real-time streaming pipelines (Kafka, Spark Streaming).
  - Build full ML-powered credit risk prediction with SHAP explanations.
  - Scale into a SaaS platform for regulators, banks, and institutional investors.


## 📂 Repo Structure

```bash
cred-intel/
├── src/
│   ├── ingest/
│   │   ├── alpha_vantage.py        # Alpha Vantage fetch (volatility, indicators)
│   │   ├── news.py                 # News + sentiment via RSS
│   │   ├── sec_edgar.py            # SEC filings fetcher
│   │   ├── worldbank.py            # World Bank + macro indicators
│   │   └── yahoo_finance.py        # Yahoo Finance fundamentals
│   │   
│   ├── model/
│   │   ├── explain.py              # SHAP + event deltas → text
│   │   ├── scorecard.py            # Interpretable scoring engine
│   │   └── tree_model.py           # Decision tree + SHAP utilities
│   |
│   ├── utils/
│   │   ├── cache.py                # Last good value, staleness
│   │   ├── config.py               # API keys, refresh interval
│   │   └── retry.py                # Retry/backoff logic
│   |
│   ├── pipeline.py                 # Fetch-all-sources aggregator
│   └── prototype.py                # Initial prototype script
│
├── data/
│   ├── snapshots/                  # Parquet snapshots by timestamp
│   └── demo.csv                    # Small demo to run offline
│
├── tests/
│   ├── test_ingest.py              # Unit tests for ingest layer
│   ├── test_features.py            # Unit tests for feature building
│   └── test_scorecard.py           # Unit tests for scorecard model
│
├── Dockerfile                      # Container spec
├── LICENSE                         # Open source license
├── PRESENTATION.pptx               # Submission deck (slides)
├── README.md                       # Documentation
├── app.py                          # Streamlit dashboard (main entry)
├── requirements.txt                # Dependencies
└── run.sh                          # Helper script (docker run)
