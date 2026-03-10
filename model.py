from models.risk_predictor import predict_risk
from models.trend_analyzer import update_risk
from models.suggestion_engine import generate_suggestions

def analyze_text(text):
    # predict_risk now returns risk, emotions dict, and mood/crisis info
    risk, emotions= predict_risk(text)
    final_risk = update_risk(risk)
    suggestions = generate_suggestions(emotions, final_risk)


    # dominant emotion for display
    if "CRISIS" in emotions:
        dominant_emotion = "CRISIS"
    else:
        dominant_emotion = max(emotions, key=emotions.get)

    return {
        "risk": round(final_risk, 3),
        "emotions": emotions,
        "emotion": dominant_emotion,
        "suggestions": suggestions
    }