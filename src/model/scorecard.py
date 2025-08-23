import numpy as np

def compute_scorecard(prob):
    # Convert probability (0–1) to credit score (0–100)
    return int(np.round(prob * 100))

def interpret_score(score):
    if score >= 75:
        return "🟢 Low Risk"
    elif score >= 50:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"


