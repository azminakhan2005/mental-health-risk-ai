import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# Example training dataset
data = {
    "sadness":[0.8,0.7,0.1,0.2],
    "anger":[0.1,0.2,0.1,0.0],
    "fear":[0.4,0.5,0.1,0.0],
    "joy":[0.1,0.0,0.7,0.8],
    "love":[0.0,0.1,0.4,0.5],
    "surprise":[0.0,0.0,0.1,0.2],
    "risk":[1,1,0,0]
}

df = pd.DataFrame(data)

X = df.drop("risk",axis=1)
y = df["risk"]

model = LogisticRegression()

model.fit(X,y)

joblib.dump(model,"models/risk_model.pkl")

print("Risk model trained")