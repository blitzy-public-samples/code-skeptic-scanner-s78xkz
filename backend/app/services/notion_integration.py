from notion_client import Client
from app.db.firestore import get_document, update_document
from app.core.config import settings

# HUMAN ASSISTANCE NEEDED
# The following function has a confidence level of 0.6 and may need adjustments for production readiness
def sync_tweet_to_notion(tweet_id: str) -> bool:
    # Retrieve tweet and response data from Firestore
    tweet_data = get_document('tweets', tweet_id)
    if not tweet_data:
        return False

    # Format data for Notion database structure
    notion_data = {
        "Tweet": {"title": [{"text": {"content": tweet_data['text']}}]},
        "Response": {"rich_text": [{"text": {"content": tweet_data.get('response', '')}}]},
        "Date": {"date": {"start": tweet_data['created_at']}},
        "Author": {"rich_text": [{"text": {"content": tweet_data['author']}}]},
    }

    # Create or update Notion database entry
    notion = Client(auth=settings.NOTION_API_KEY)
    database_id = settings.NOTION_DATABASE_ID

    try:
        notion.pages.create(
            parent={"database_id": database_id},
            properties=notion_data
        )
    except Exception as e:
        print(f"Error syncing to Notion: {str(e)}")
        return False

    # Update Firestore with Notion sync status
    update_document('tweets', tweet_id, {'notion_synced': True})

    return True

# HUMAN ASSISTANCE NEEDED
# The following function has a confidence level of 0.7 and may need adjustments for production readiness
def create_notion_notification(tweet_id: str, notification_type: str) -> bool:
    notion = Client(auth=settings.NOTION_API_KEY)
    notifications_database_id = settings.NOTION_NOTIFICATIONS_DATABASE_ID

    # Retrieve tweet data from Firestore
    tweet_data = get_document('tweets', tweet_id)
    if not tweet_data:
        return False

    # Construct notification content based on type
    if notification_type == 'new_tweet':
        title = f"New Tweet: {tweet_data['text'][:50]}..."
        content = f"A new tweet has been posted: {tweet_data['text']}"
    elif notification_type == 'new_response':
        title = f"New Response: {tweet_data['response'][:50]}..."
        content = f"A new response has been generated for tweet: {tweet_data['text']}\n\nResponse: {tweet_data['response']}"
    else:
        return False

    # Create new page in Notion notifications database
    try:
        notion.pages.create(
            parent={"database_id": notifications_database_id},
            properties={
                "Title": {"title": [{"text": {"content": title}}]},
                "Content": {"rich_text": [{"text": {"content": content}}]},
                "Type": {"select": {"name": notification_type}},
                "Date": {"date": {"start": tweet_data['created_at']}},
            }
        )
    except Exception as e:
        print(f"Error creating Notion notification: {str(e)}")
        return False

    return True