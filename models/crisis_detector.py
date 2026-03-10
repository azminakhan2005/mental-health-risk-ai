import pandas as pd

# Load crisis dataset
df = pd.read_csv("data/crisis_phrases.tsv", sep="\t")

# Convert column to list
CRISIS_PHRASES = df["text"].str.lower().tolist()


def detect_crisis(text):
    text = text.lower().strip()

    for phrase in CRISIS_PHRASES:
        if phrase in text:
            return True

    return False