# rss.py
# News + sentiment + event tags

import feedparser

def fetch_rss_feed(url: str):
    """
    Fetch news articles from an RSS feed.
    """
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "")
        })
    return articles

