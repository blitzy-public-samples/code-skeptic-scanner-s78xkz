import React, { useState, useEffect } from 'react';
import { TweetList } from '../components/TweetList';
import { AnalyticsChart } from '../components/AnalyticsChart';
import { fetchTweets, fetchAnalytics } from '../services/api';
import { useSelector, useDispatch } from '../store/tweetSlice';

// HUMAN ASSISTANCE NEEDED
// The following component may need additional refinement for production readiness.
// Please review and adjust as necessary.

const Dashboard: React.FC = () => {
  const [tweets, setTweets] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any>({});
  const dispatch = useDispatch();
  const tweetState = useSelector((state: any) => state.tweets);

  useEffect(() => {
    const loadData = async () => {
      try {
        const fetchedTweets = await fetchTweets();
        setTweets(fetchedTweets);
        dispatch({ type: 'SET_TWEETS', payload: fetchedTweets });

        const fetchedAnalytics = await fetchAnalytics();
        setAnalytics(fetchedAnalytics);
      } catch (error) {
        console.error('Error fetching data:', error);
        // TODO: Implement proper error handling
      }
    };

    loadData();
  }, [dispatch]);

  return (
    <div className="dashboard">
      <h1>Tweet Monitoring Dashboard</h1>
      <div className="dashboard-summary">
        <h2>Summary Statistics</h2>
        {/* TODO: Add summary statistics here */}
      </div>
      <div className="dashboard-main">
        <div className="tweet-list-container">
          <h2>Recent Tweets</h2>
          <TweetList tweets={tweets} />
        </div>
        <div className="analytics-chart-container">
          <h2>Tweet Analytics</h2>
          <AnalyticsChart data={analytics} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;