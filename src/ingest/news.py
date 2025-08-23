import urllib.parse, feedparser
from textblob import TextBlob
from typing import Dict, Any, List

def sentiment_of_text(text: str) -> float:
    if not text: return 0.0
    return TextBlob(text).sentiment.polarity

def avg(lst: List[float], default=0.0):
    return sum(lst)/len(lst) if lst else default

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
        q = urllib.parse.quote(f'{company} press release')
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={q}")
        titles = [e.title for e in feed.entries[:8]]
        sents  = [sentiment_of_text(t) for t in titles]
        return {"PR_count": len(titles), "PR_sent": avg(sents)}
    except: return {"PR_count":0,"PR_sent":0.0}
