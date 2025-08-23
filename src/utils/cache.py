from functools import lru_cache
import time

@lru_cache(maxsize=100)
def cached_request(url, timeout=15):
    import requests
    res = requests.get(url, timeout=timeout)
    return res.json()
