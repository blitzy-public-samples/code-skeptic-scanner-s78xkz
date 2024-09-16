from tweepy import Stream
from google.cloud.pubsub_v1 import PublisherClient
from app.core.config import settings
from app.db.firestore import add_document

class TweetListener:
    def __init__(self, publisher: PublisherClient, topic_path: str):
        self.publisher = publisher
        self.topic_path = topic_path
        self.ai_coding_tools_keywords = ["ChatGPT", "GitHub Copilot", "Tabnine", "Kite", "CodeWhisperer"]

    # HUMAN ASSISTANCE NEEDED
    # The confidence level for this function is below 0.8. Please review and adjust as necessary.
    def on_status(self, status: tweepy.Status) -> bool:
        # Check if tweet meets popularity threshold (e.g., retweets, likes)
        if status.retweet_count + status.favorite_count < settings.TWEET_POPULARITY_THRESHOLD:
            return True

        # Extract relevant information from tweet
        tweet_data = {
            "id": status.id_str,
            "text": status.text,
            "user": status.user.screen_name,
            "created_at": status.created_at.isoformat(),
            "retweet_count": status.retweet_count,
            "favorite_count": status.favorite_count,
        }

        # Publish tweet data to Pub/Sub topic
        self.publisher.publish(self.topic_path, data=json.dumps(tweet_data).encode("utf-8"))

        # Store raw tweet data in Firestore
        add_document("raw_tweets", tweet_data)

        return True

# HUMAN ASSISTANCE NEEDED
# The confidence level for this function is below 0.8. Please review and adjust as necessary.
def start_tweet_stream():
    publisher = PublisherClient()
    topic_path = publisher.topic_path(settings.GCP_PROJECT_ID, settings.PUBSUB_TOPIC)

    listener = TweetListener(publisher, topic_path)

    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)
    stream.filter(track=listener.ai_coding_tools_keywords)