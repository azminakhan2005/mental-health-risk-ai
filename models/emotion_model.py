from transformers import pipeline

emotion_pipeline = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None
)

def extract_features(text):

    results = emotion_pipeline(text)

    if isinstance(results[0], list):
        results = results[0]

    emotions = {}

    for r in results:
        label = r["label"]
        score = r["score"]
        emotions[label] = float(score)

    return emotions