import React, { useState, useEffect } from 'react';
import TweetCard from '../components/TweetCard';
import { Tweet, TweetListProps } from '../schema/types';

const TweetList: React.FC<TweetListProps> = ({ tweets, onFilterChange, onSortChange }) => {
  const [filteredTweets, setFilteredTweets] = useState<Tweet[]>(tweets);
  const [sortOption, setSortOption] = useState<string>('latest');
  const [filterOption, setFilterOption] = useState<string>('all');

  useEffect(() => {
    let sorted = [...tweets];
    if (sortOption === 'latest') {
      sorted.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
    } else if (sortOption === 'popular') {
      sorted.sort((a, b) => b.likes - a.likes);
    }

    if (filterOption !== 'all') {
      sorted = sorted.filter(tweet => tweet.category === filterOption);
    }

    setFilteredTweets(sorted);
  }, [tweets, sortOption, filterOption]);

  const handleSortChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSortOption(event.target.value);
    onSortChange(event.target.value);
  };

  const handleFilterChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setFilterOption(event.target.value);
    onFilterChange(event.target.value);
  };

  return (
    <div className="tweet-list">
      <div className="tweet-list-controls">
        <select onChange={handleFilterChange} value={filterOption}>
          <option value="all">All Categories</option>
          <option value="tech">Tech</option>
          <option value="sports">Sports</option>
          <option value="news">News</option>
        </select>
        <select onChange={handleSortChange} value={sortOption}>
          <option value="latest">Latest</option>
          <option value="popular">Popular</option>
        </select>
      </div>
      {filteredTweets.map(tweet => (
        <TweetCard key={tweet.id} tweet={tweet} />
      ))}
      {/* HUMAN ASSISTANCE NEEDED */}
      {/* Implement pagination or infinite scroll here */}
      {/* This part requires more context about the desired UX and available backend API */}
    </div>
  );
};

export default TweetList;