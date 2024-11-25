import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for macOS or server environments
import matplotlib.pyplot as plt
import pandas as pd
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import praw

def reddit_sentiment_score(data):
    """
    Calculate sentiment scores for a list of text data.
    Args:
        data (list of str): List of text (e.g., Reddit post title, body, and comments).
    Returns:
        dict: Sentiment scores for positive, negative, and neutral percentages.
    """
    # Initialize VADER sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Analyze sentiment
    positive_count, negative_count, neutral_count = 0, 0, 0
    for text in data:
        scores = sid.polarity_scores(text)
        if scores['compound'] >= 0.05:
            positive_count += 1
        elif scores['compound'] <= -0.05:
            negative_count += 1
        else:
            neutral_count += 1

    # Calculate percentages
    total_count = positive_count + negative_count + neutral_count
    sentiment_scores = {
        'pos': (positive_count / total_count) * 100 if total_count > 0 else 0,
        'neg': (negative_count / total_count) * 100 if total_count > 0 else 0,
        'neu': (neutral_count / total_count) * 100 if total_count > 0 else 0
    }

    print(f"Sentiment Scores: {sentiment_scores}")
    return sentiment_scores

