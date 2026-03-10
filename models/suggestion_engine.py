def generate_suggestions(emotions, risk):

    suggestions = []

    dominant = max(emotions, key=emotions.get)

    # Crisis handling
    if dominant == "CRISIS":
        suggestions.append("Immediate help needed! Call a helpline or trusted friend.")
        suggestions.append("Reach out to a mental health professional now.")
        suggestions.append("Do not be alone — stay in a safe environment.")
        return suggestions[:3]

    # emotion-based suggestions

    if emotions.get("sadness",0) > 0.4:
        suggestions.append("Try writing about what is making you feel sad. Journaling helps process emotions.")

    if emotions.get("nervousness",0) > 0.4:
        suggestions.append("Practice slow breathing or take a short break to reduce stress.")

    if emotions.get("anger",0) > 0.4:
        suggestions.append("Step away for a few minutes and do something calming like a short walk.")

    if emotions.get("fear",0) > 0.4:
        suggestions.append("Talk to a trusted friend or family member about your worries.")

    if emotions.get("joy",0) > 0.4:
        suggestions.append("Keep doing things that make you happy and maintain this positive routine.")

    # risk-level suggestions
    if risk < 0.3:
        suggestions.append("You seem emotionally stable. Keep maintaining healthy routines.")

    elif risk < 0.5:
        suggestions.append("You might be experiencing mild stress. Consider relaxation or mindfulness.")

    elif risk < 0.65:
        suggestions.append("Stress levels appear elevated. Consider taking breaks and getting enough sleep.")

    else:
        suggestions.append("Your recent entries suggest persistent distress. Consider consulting a mental health professional.")

    return suggestions