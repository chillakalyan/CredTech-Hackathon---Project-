# scorecard.py
# Interpretable scoring functions

import pandas as pd

def calculate_score(features: pd.DataFrame) -> pd.DataFrame:
    """
    Simple interpretable scorecard:
    - Assigns points based on feature thresholds.
    """
    scores = []
    for _, row in features.iterrows():
        score = 0
        if "Close" in row and row["Close"] > 0.5:
            score += 10
        if "GDP" in row and row["GDP"] > 2.0:
            score += 15
        if "Unemployment" in row and row["Unemployment"] < 5.0:
            score += 10
        scores.append(score)
    features["score"] = scores
    return features

