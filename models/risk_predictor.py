import joblib
import numpy as np
from models.emotion_model import extract_features
from models.crisis_detector import detect_crisis

# Load trained logistic regression model
model = joblib.load("models/risk_model.pkl")

# All emotions
EMOTIONS = [
    "admiration","amusement","anger","annoyance","approval","caring","confusion",
    "curiosity","desire","disappointment","disapproval","disgust","embarrassment",
    "excitement","fear","gratitude","grief","joy","love","nervousness",
    "optimism","pride","realization","relief","remorse","sadness","surprise","neutral"
]

# Positive and negative emotion sets
POSITIVE = [
    "joy","optimism","gratitude","love","excitement",
    "relief","admiration","amusement","approval","caring","pride"
]

NEGATIVE = [
    "sadness","grief","fear","anger","disappointment",
    "remorse","nervousness","disgust","annoyance","embarrassment"
]

def predict_risk(text):

    emotions = extract_features(text)

    # Crisis override
    if detect_crisis(text):
        emotions = {k: 0 for k in EMOTIONS}
        emotions["CRISIS"] = 1.0
        return 1.0, emotions

    # Emotion balance
    pos_score = sum(emotions.get(e, 0) for e in POSITIVE)
    neg_score = sum(emotions.get(e, 0) for e in NEGATIVE)

    total = pos_score + neg_score
    if total > 0:
        pos_norm = pos_score / total
        neg_norm = neg_score / total
    else:
        pos_norm = 0
        neg_norm = 0

    # ML feature vector
    X = np.array([[emotions.get(k, 0) for k in EMOTIONS]])

    # Predict class
    risk_class = model.predict(X)[0]

    # Convert class → risk score
    risk_map = {
        0: 0.2,   # positive / neutral
        1: 0.4,   # mild distress
        2: 0.6,   # moderate distress
        3: 0.85   # severe distress
    }

    risk = risk_map.get(risk_class, 0.4)

    # Small adjustment from emotion balance
    risk += (0.08 * neg_norm - 0.10 * pos_norm)

    # Clamp between 0 and 1
    risk = max(0, min(1, risk))

    return risk, emotions