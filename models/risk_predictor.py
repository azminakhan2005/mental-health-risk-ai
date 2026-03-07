import joblib
from models.bert_features import extract_features

model = joblib.load("models/risk_model.pkl")

def predict_risk(text):

    features = extract_features(text)

    X = [[
        features["sadness"],
        features["anger"],
        features["fear"],
        features["joy"],
        features["love"],
        features["surprise"]
    ]]

    probability = model.predict_proba(X)[0][1]

    return probability, features