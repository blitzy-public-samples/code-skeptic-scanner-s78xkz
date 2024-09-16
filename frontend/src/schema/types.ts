import { ReactNode } from 'react';

export interface Tweet {
  id: string;
  accountHandle: string;
  followersCount: number;
  likesCount: number;
  timestamp: Date;
  content: string;
  mediaUrls: string[];
  quotedTweetContent: string | null;
  doubtRating: number;
  aiToolsMentioned: string[];
}

export interface Response {
  id: string;
  tweetId: string;
  content: string;
  generatedAt: Date;
  status: ResponseStatus;
  generatedBy: string;
}

export interface Context {
  id: string;
  name: string;
  content: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Prompt {
  id: string;
  name: string;
  content: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface User {
  id: string;
  username: string;
  email: string;
  role: UserRole;
  lastLogin: Date;
}

export enum ResponseStatus {
  pending = 'pending',
  approved = 'approved',
  posted = 'posted'
}

export enum UserRole {
  admin = 'admin',
  analyst = 'analyst',
  moderator = 'moderator',
  viewer = 'viewer'
}

export type TweetListProps = {
  tweets: Tweet[];
  onSelectTweet: (tweetId: string) => void;
}

// HUMAN ASSISTANCE NEEDED
// The confidence level for ResponseGeneratorProps is 0.8, which is below the threshold.
// Please review and adjust the following type definition if necessary.
export type ResponseGeneratorProps = {
  selectedTweet: Tweet;
  contexts: Context[];
  prompts: Prompt[];
  onResponseGenerated: (response: Response) => void;
}