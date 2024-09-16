from google.cloud.language_v1 import LanguageServiceClient
from app.db.firestore import update_document
from app.core.config import settings

# HUMAN ASSISTANCE NEEDED
# The following function has a confidence level below 0.8 and may need refinement for production readiness
def analyze_tweet(tweet_data: dict) -> dict:
    # Initialize Google Cloud Natural Language client
    client = LanguageServiceClient()

    # Perform sentiment analysis on tweet content
    document = client.document_from_text(tweet_data['content'])
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    # Calculate doubt rating based on sentiment and keywords
    doubt_keywords = settings.DOUBT_KEYWORDS
    doubt_rating = 0
    for keyword in doubt_keywords:
        if keyword.lower() in tweet_data['content'].lower():
            doubt_rating += 1
    
    doubt_rating = min(doubt_rating / len(doubt_keywords) + (1 - sentiment.score) / 2, 1)

    # Update tweet data with analysis results
    analyzed_tweet = tweet_data.copy()
    analyzed_tweet['sentiment_score'] = sentiment.score
    analyzed_tweet['sentiment_magnitude'] = sentiment.magnitude
    analyzed_tweet['doubt_rating'] = doubt_rating

    # Update tweet document in Firestore with analysis results
    update_document('tweets', tweet_data['id'], analyzed_tweet)

    return analyzed_tweet

def identify_ai_tools(tweet_content: str) -> list:
    ai_tools = settings.AI_TOOLS_KEYWORDS
    identified_tools = []

    for tool, keywords in ai_tools.items():
        for keyword in keywords:
            if keyword.lower() in tweet_content.lower():
                identified_tools.append(tool)
                break

    return identified_tools