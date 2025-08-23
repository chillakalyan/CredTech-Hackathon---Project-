import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def train_tree_model(data_path):
    df = pd.read_csv(data_path)
    X = df[["DebtToEquity", "PE_Ratio", "ProfitMargins", "News_sent", "PR_sent"]]
    y = (df["Score"] > 50).astype(int)   # Example: classify companies as High/Low risk

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    print("✅ Model trained")
    print(classification_report(y_test, model.predict(X_test)))

    return model

