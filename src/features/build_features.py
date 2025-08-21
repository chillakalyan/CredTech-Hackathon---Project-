# build_features.py
# Normalization, winsorize, joins

import pandas as pd
import numpy as np

def normalize_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Normalize a column to 0-1 range.
    """
    if column in df.columns:
        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min() + 1e-9)
    return df

def winsorize_column(df: pd.DataFrame, column: str, lower=0.05, upper=0.95) -> pd.DataFrame:
    """
    Winsorize column values to reduce outliers.
    """
    if column in df.columns:
        lower_val = df[column].quantile(lower)
        upper_val = df[column].quantile(upper)
        df[column] = np.clip(df[column], lower_val, upper_val)
    return df

def build_features(price_data: pd.DataFrame, macro_data: pd.DataFrame) -> pd.DataFrame:
    """
    Merge and preprocess datasets into a feature set.
    """
    try:
        df = price_data.copy()
        if not macro_data.empty:
            df = df.merge(macro_data, left_index=True, right_index=True, how="left")
        # Example normalization
        if "Close" in df.columns:
            df = normalize_column(df, "Close")
        return df
    except Exception as e:
        print(f"Error building features: {e}")
        return pd.DataFrame()

