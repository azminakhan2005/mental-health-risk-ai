from transformers import pipeline

# Load BERT emotion model
emotion_model = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    return_all_scores=True
)

def extract_features(text):

    results = emotion_model(text)

    # results format -> [[{label,score}, {label,score}...]]
    results = results[0]

    features = {
        "sadness":0,
        "anger":0,
        "fear":0,
        "joy":0,
        "love":0,
        "surprise":0
    }

    for r in results:

        if isinstance(r, dict):
            label = r["label"]
            score = r["score"]

            if label in features:
                features[label] = score

    return features