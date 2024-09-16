import React, { useEffect } from 'react';
import { Dashboard } from '../components/Dashboard';
import { TweetList } from '../components/TweetList';
import { fetchTweets } from '../services/api';
import { useSelector, useDispatch } from '../store/tweetSlice';

const Home: React.FC = () => {
  const dispatch = useDispatch();
  const tweets = useSelector((state) => state.tweets.tweets);

  useEffect(() => {
    const loadTweets = async () => {
      try {
        const fetchedTweets = await fetchTweets();
        dispatch({ type: 'tweets/setTweets', payload: fetchedTweets });
      } catch (error) {
        console.error('Failed to fetch tweets:', error);
        // HUMAN ASSISTANCE NEEDED
        // TODO: Implement proper error handling and user feedback
      }
    };

    loadTweets();
  }, [dispatch]);

  return (
    <div className="home-container">
      <Dashboard />
      <TweetList tweets={tweets} />
    </div>
  );
};

export default Home;