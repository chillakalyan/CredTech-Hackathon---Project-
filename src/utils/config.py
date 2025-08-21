# config.py
# API keys, refresh intervals

API_KEYS = {
    "fred": "YOUR_FRED_API_KEY",
    "world_bank": "YOUR_WORLD_BANK_KEY"
}

REFRESH_INTERVALS = {
    "yfinance": 60,       # in minutes
    "fred": 1440,         # once per day
    "rss": 30             # every 30 minutes
}

