# retry.py
# Retry with exponential backoff

import time
import functools

def retry(max_attempts=3, delay=1, backoff=2):
    """
    Retry decorator with exponential backoff.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts, wait = 0, delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}, retrying in {wait}s...")
                    time.sleep(wait)
                    wait *= backoff
                    attempts += 1
            raise Exception(f"Function {func.__name__} failed after {max_attempts} attempts")
        return wrapper
    return decorator

