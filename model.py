from models.risk_predictor import predict_risk
from models.suggestions import generate_suggestions

daily_risks = []

def analyze_text(text):

    risk, emotions = predict_risk(text)

    daily_risks.append(risk)

    avg_risk = sum(daily_risks) / len(daily_risks)

    # generate suggestions
    suggestions = generate_suggestions(emotions, risk)

    return {

        "emotion_scores": emotions,
        "risk": risk,
        "daily_risk": avg_risk,
        "suggestions": suggestions}
