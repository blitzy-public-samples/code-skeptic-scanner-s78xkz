import pytest
from unittest.mock import patch, MagicMock
from app.tasks import process_tweet, sync_to_notion, cleanup_old_data
from app.models import Tweet, NotionPage
from datetime import datetime, timedelta

@pytest.fixture
def mock_tweet():
    return Tweet(id=1, content="Test tweet", created_at=datetime.now())

@pytest.fixture
def mock_notion_page():
    return NotionPage(id="page_id", tweet_id=1, last_synced=datetime.now())

@pytest.mark.asyncio
async def test_process_tweet(mock_tweet):
    with patch('app.tasks.analyze_sentiment') as mock_analyze:
        mock_analyze.return_value = 0.8
        result = await process_tweet(mock_tweet)
        assert result == 0.8
        mock_analyze.assert_called_once_with(mock_tweet.content)

@pytest.mark.asyncio
async def test_sync_to_notion(mock_tweet, mock_notion_page):
    with patch('app.tasks.notion_client.pages.create') as mock_create, \
         patch('app.tasks.notion_client.pages.update') as mock_update:
        
        mock_create.return_value = {"id": "new_page_id"}
        mock_update.return_value = {"id": "updated_page_id"}

        # Test creating a new page
        result = await sync_to_notion(mock_tweet)
        assert result == "new_page_id"
        mock_create.assert_called_once()

        # Test updating an existing page
        result = await sync_to_notion(mock_tweet, mock_notion_page)
        assert result == "updated_page_id"
        mock_update.assert_called_once()

@pytest.mark.asyncio
async def test_cleanup_old_data():
    with patch('app.models.Tweet.delete') as mock_tweet_delete, \
         patch('app.models.NotionPage.delete') as mock_notion_delete:
        
        cutoff_date = datetime.now() - timedelta(days=30)
        
        mock_tweet_delete.return_value = 5
        mock_notion_delete.return_value = 3

        deleted_tweets, deleted_pages = await cleanup_old_data(cutoff_date)
        
        assert deleted_tweets == 5
        assert deleted_pages == 3
        
        mock_tweet_delete.assert_called_once_with(Tweet.created_at < cutoff_date)
        mock_notion_delete.assert_called_once_with(NotionPage.last_synced < cutoff_date)

# HUMAN ASSISTANCE NEEDED
# The following test cases might need additional assertions or edge case handling:
# - Test process_tweet with various sentiment scores
# - Test sync_to_notion with API errors or rate limiting
# - Test cleanup_old_data with no data to delete
# Consider adding these test cases for more comprehensive coverage.