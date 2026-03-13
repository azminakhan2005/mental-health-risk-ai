import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "models/crisis_model.pkl"
VEC_PATH = "models/vectorizer.pkl"
DATA_PATH = "data/suicide_detection.csv"


def train_model():

    # load dataset
    df = pd.read_csv(DATA_PATH)

    # convert text to lowercase
    df["text"] = df["text"].str.lower()

    # convert labels
    df["class"] = df["class"].map({
        "suicide": 1,
        "non-suicide": 0
    })

    X = df["text"]
    y = df["class"]

    # convert text → numeric features
    vectorizer = TfidfVectorizer(stop_words="english")

    X_vec = vectorizer.fit_transform(X)

    # train ML model
    model = LogisticRegression(max_iter=1000)

    model.fit(X_vec, y)

    # save trained model
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VEC_PATH)

    return model, vectorizer

if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VEC_PATH)

else:

    model, vectorizer = train_model()


def detect_crisis(text):

    text = text.lower().strip()

    X = vectorizer.transform([text])

    prob = model.predict_proba(X)[0][1]

    if prob > 0.90:
        return True

    return False