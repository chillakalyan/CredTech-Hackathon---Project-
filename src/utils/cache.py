# cache.py
# Last good value, staleness check

import pandas as pd
from datetime import datetime, timedelta

class Cache:
    def __init__(self, max_age_minutes=60):
        self.data = None
        self.timestamp = None
        self.max_age = timedelta(minutes=max_age_minutes)

    def set(self, data):
        self.data = data
        self.timestamp = datetime.now()

    def get(self):
        if self.timestamp and datetime.now() - self.timestamp < self.max_age:
            return self.data
        return None

    def is_stale(self):
        if not self.timestamp:
            return True
        return datetime.now() - self.timestamp > self.max_age

