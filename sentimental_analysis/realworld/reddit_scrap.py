from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
import nltk
import matplotlib
import os
matplotlib.use('Agg')  # Use a non-GUI backend for macOS or server environments


def reddit_sentiment_score(data):
    """
    Calculate sentiment scores for a list of text data.
    Args:
        data (list of str): List of text (e.g.,
          Reddit post title, body, and comments).
    Returns:
        dict: Sentiment scores for positive, negative, and neutral percentages.
    """
    # Ensure the necessary NLTK data is downloaded
    nltk.download('vader_lexicon')
    nltk.download('punkt')

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


def fetch_reddit_post(post_url):
    """
    Fetch the content of a specific Reddit post using its URL.
    """
    reddit = praw.Reddit(
        client_id=os.environ.get('REDDIT_CLIENT_ID'),
        # Replace with your Reddit API client ID
        client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
        # Replace with your Reddit API client secret
        user_agent=os.environ.get('REDDIT_USER_AGENT')
        # Replace with your user agent
    )

    # Fetch the specific post using the URL
    submission = reddit.submission(url=post_url)
    post_content = {
        "title": submission.title,
        "body": submission.selftext,
        "comments": [
            comment.body for comment in submission.comments.list()[:10]
        ],  # Fetch top 10 comments
    }
    return post_content
