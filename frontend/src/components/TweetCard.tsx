import React from 'react';
import { Tweet } from '../schema/types';
import { formatDate, formatNumber } from '../utils/formatters';

const TweetCard: React.FC<{ tweet: Tweet }> = ({ tweet }) => {
  return (
    <div className="tweet-card">
      <div className="tweet-content">{tweet.content}</div>
      <div className="tweet-account">
        <span className="account-handle">@{tweet.accountHandle}</span>
        <span className="follower-count">{formatNumber(tweet.followerCount)} followers</span>
      </div>
      <div className="tweet-meta">
        <span className="timestamp">{formatDate(tweet.timestamp)}</span>
        <span className="like-count">{formatNumber(tweet.likeCount)} likes</span>
      </div>
      {tweet.mediaContent && (
        <div className="tweet-media">
          {tweet.mediaContent.type === 'image' && (
            <img src={tweet.mediaContent.url} alt="Tweet media" />
          )}
          {tweet.mediaContent.type === 'video' && (
            <video src={tweet.mediaContent.url} controls />
          )}
        </div>
      )}
      <div className="tweet-analysis">
        <div className="doubt-rating">Doubt Rating: {tweet.doubtRating.toFixed(2)}</div>
        {tweet.aiToolsMentioned.length > 0 && (
          <div className="ai-tools">
            AI Tools Mentioned:
            <ul>
              {tweet.aiToolsMentioned.map((tool, index) => (
                <li key={index}>{tool}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default TweetCard;