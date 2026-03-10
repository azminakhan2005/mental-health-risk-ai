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
    """
    Returns:
        risk: float [0-1]
        emotions: dict of emotion scores (+ CRISIS if detected)
    """

    # Extract emotions from text
    emotions = extract_features(text)

    # Crisis detection override
    if detect_crisis(text):
        emotions = {k: 0 for k in EMOTIONS}
        emotions["CRISIS"] = 1.0
        return 1.0, emotions

    # Weighted adjustment based on positive vs negative emotions
    pos_score = sum([emotions.get(e, 0) for e in POSITIVE])
    neg_score = sum([emotions.get(e, 0) for e in NEGATIVE])

    total = pos_score + neg_score
    if total > 0:
        pos_norm = pos_score / total
        neg_norm = neg_score / total
    else:
        pos_norm = 0
        neg_norm = 0

    # Feature vector for ML model
    X = np.array([[emotions.get(k, 0) for k in EMOTIONS]])

    # Predict base probability
    base_prob = model.predict_proba(X)[0][1]

    # Adjust risk based on positive/negative balance
    # Negatives increase risk, positives reduce it slightly
    risk = base_prob * (1 + 0.2*neg_norm - 0.2*pos_norm)

    # Clamp between 0 and 1
    risk = min(max(round(risk, 2), 0), 1)

    # Avoid too-low predictions
    risk = max(risk, 0.1)

    return risk, emotions