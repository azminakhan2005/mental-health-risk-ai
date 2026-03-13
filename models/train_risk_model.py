import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
df = pd.read_csv("data/risk_training.tsv", sep="\t")

# Features & target
X = df.drop("risk", axis=1)
y = df["risk"]

model = LogisticRegression(max_iter=2000)
model.fit(X, y)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/risk_model.pkl")

print("Risk model trained successfully")