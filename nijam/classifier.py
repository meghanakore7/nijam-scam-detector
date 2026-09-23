"""
classifier.py
--------------
Trains a lightweight TF-IDF + Naive Bayes text classifier on the sample
labeled dataset (data/messages.csv) to estimate the probability that a
given message is a scam, purely from language patterns (word choice,
phrasing) rather than explicit rule keywords.

This complements rules.py: rules catch known, explainable red flags,
while this model can catch scam-like *phrasing* even when it doesn't
match an exact keyword.

In a production version this would be trained on a much larger, more
diverse, real-world dataset (with consent and privacy safeguards) rather
than the small illustrative sample included here.
"""

import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "messages.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "model.joblib")


def train_model(data_path: str = DATA_PATH, model_path: str = MODEL_PATH):
    """Train the TF-IDF + Naive Bayes pipeline and save it to disk."""
    df = pd.read_csv(data_path)

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", MultinomialNB()),
        ]
    )
    pipeline.fit(df["text"], df["label"])

    joblib.dump(pipeline, model_path)
    return pipeline


def load_model(model_path: str = MODEL_PATH):
    """Load a trained model from disk, training one first if missing."""
    if not os.path.exists(model_path):
        return train_model()
    return joblib.load(model_path)


def predict_scam_probability(text: str, model=None) -> float:
    """Return the model's estimated probability that `text` is a scam (0-1)."""
    if model is None:
        model = load_model()

    proba = model.predict_proba([text])[0]
    classes = list(model.classes_)
    scam_index = classes.index("scam")
    return float(proba[scam_index])


if __name__ == "__main__":
    print("Training model on sample dataset...")
    train_model()
    print(f"Model saved to {MODEL_PATH}")
