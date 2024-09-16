import unittest
from unittest.mock import patch, MagicMock
from services.tweet_ingestion import TweetIngestionService
from services.tweet_analysis import TweetAnalysisService
from services.response_generation import ResponseGenerationService
from services.notion_integration import NotionIntegrationService

class TestTweetIngestionService(unittest.TestCase):
    def setUp(self):
        self.ingestion_service = TweetIngestionService()

    @patch('tweepy.API')
    def test_fetch_tweets(self, mock_api):
        mock_api.search_tweets.return_value = [MagicMock(id=1, text='Test tweet')]
        tweets = self.ingestion_service.fetch_tweets('test query')
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0].text, 'Test tweet')

    def test_preprocess_tweet(self):
        tweet = MagicMock(text='Test #tweet with @mention')
        processed_tweet = self.ingestion_service.preprocess_tweet(tweet)
        self.assertEqual(processed_tweet, 'Test tweet with mention')

class TestTweetAnalysisService(unittest.TestCase):
    def setUp(self):
        self.analysis_service = TweetAnalysisService()

    def test_analyze_sentiment(self):
        tweet = 'I love this product!'
        sentiment = self.analysis_service.analyze_sentiment(tweet)
        self.assertIn(sentiment, ['positive', 'negative', 'neutral'])

    def test_extract_keywords(self):
        tweet = 'AI and machine learning are revolutionizing technology'
        keywords = self.analysis_service.extract_keywords(tweet)
        self.assertIn('AI', keywords)
        self.assertIn('machine learning', keywords)

class TestResponseGenerationService(unittest.TestCase):
    def setUp(self):
        self.response_service = ResponseGenerationService()

    @patch('openai.Completion.create')
    def test_generate_response(self, mock_completion):
        mock_completion.return_value = MagicMock(choices=[MagicMock(text='Generated response')])
        tweet = 'Test tweet'
        response = self.response_service.generate_response(tweet)
        self.assertEqual(response, 'Generated response')

class TestNotionIntegrationService(unittest.TestCase):
    def setUp(self):
        self.notion_service = NotionIntegrationService()

    @patch('notion_client.Client')
    def test_create_page(self, mock_client):
        mock_client.return_value.pages.create.return_value = {'id': 'page_id'}
        page_id = self.notion_service.create_page('Test Page', 'Content')
        self.assertEqual(page_id, 'page_id')

    @patch('notion_client.Client')
    def test_update_page(self, mock_client):
        mock_client.return_value.pages.update.return_value = {'id': 'page_id'}
        updated = self.notion_service.update_page('page_id', 'Updated Content')
        self.assertTrue(updated)

if __name__ == '__main__':
    unittest.main()