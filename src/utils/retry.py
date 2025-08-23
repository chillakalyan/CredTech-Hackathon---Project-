import time, requests
from functools import wraps

def retry_request(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator

@retry_request(max_retries=3, delay=5)
def safe_get(url, headers=None, timeout=15):
    return requests.get(url, headers=headers, timeout=timeout)
