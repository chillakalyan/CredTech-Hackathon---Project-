# tree_model.py
# Optional decision tree + SHAP utils

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import shap

class TreeModel:
    def __init__(self, max_depth=3):
        self.model = DecisionTreeClassifier(max_depth=max_depth)

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame):
        return self.model.predict(X)

    def explain(self, X: pd.DataFrame):
        """
        Generate SHAP explanations.
        """
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)
        return shap_values

