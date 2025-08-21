# explain.py
# SHAP + event deltas → text explanations

import shap
import pandas as pd

def shap_to_text(shap_values, feature_names, row_idx=0):
    """
    Convert SHAP values for a row into a human-readable explanation.
    """
    explanations = []
    row_shap = shap_values[row_idx]
    for val, feature in sorted(zip(row_shap, feature_names), key=lambda x: abs(x[0]), reverse=True):
        if val > 0:
            explanations.append(f"{feature} contributed positively ({val:.2f})")
        else:
            explanations.append(f"{feature} contributed negatively ({val:.2f})")
    return explanations[:5]  # return top 5 drivers

