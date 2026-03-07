def generate_suggestions(scores, risk):

    tips = []

    if scores["sadness"] > 0.5:
        tips.append("Try writing your thoughts in a journal.")

    if scores["fear"] > 0.5:
        tips.append("Practice slow breathing for a few minutes.")

    if scores["anger"] > 0.5:
        tips.append("Take a short walk to release tension.")

    if risk > 0.7:
        tips.append("Consider speaking to a counselor or trusted person.")

    return tips