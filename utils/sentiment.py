import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    if not text or not isinstance(text, str):
        return "Neutral"

    scores = sia.polarity_scores(text)
    compound = scores['compound']

    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"
    


