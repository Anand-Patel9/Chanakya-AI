from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")


def analyze_sentiment(text):

    result = sentiment_model(text[:512])[0]

    label = result["label"]

    score = result["score"]

    if label == "POSITIVE":
        return "Bullish", score

    elif label == "NEGATIVE":
        return "Bearish", score

    return "Neutral", score