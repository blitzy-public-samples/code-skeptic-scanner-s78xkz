import axios from 'axios';
import { Tweet, Response, Context, Prompt, User } from 'app/schema/types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const fetchTweets = async (page: number, limit: number): Promise<Tweet[]> => {
  const url = `${API_BASE_URL}/tweets?page=${page}&limit=${limit}`;
  const response = await axios.get(url);
  return response.data;
};

export const generateResponse = async (tweetId: string): Promise<Response> => {
  const url = `${API_BASE_URL}/responses/generate`;
  const response = await axios.post(url, { tweetId });
  return response.data;
};

export const updateResponse = async (responseId: string, updatedData: Partial<Response>): Promise<Response> => {
  const url = `${API_BASE_URL}/responses/${responseId}`;
  const response = await axios.put(url, updatedData);
  return response.data;
};

export const fetchContexts = async (): Promise<Context[]> => {
  const url = `${API_BASE_URL}/contexts`;
  const response = await axios.get(url);
  return response.data;
};

export const fetchPrompts = async (): Promise<Prompt[]> => {
  const url = `${API_BASE_URL}/prompts`;
  const response = await axios.get(url);
  return response.data;
};

// HUMAN ASSISTANCE NEEDED
// This function might need additional error handling and data validation
export const fetchAnalytics = async (metric: string, startDate: Date, endDate: Date): Promise<any> => {
  const url = `${API_BASE_URL}/analytics?metric=${metric}&startDate=${startDate.toISOString()}&endDate=${endDate.toISOString()}`;
  const response = await axios.get(url);
  return response.data;
};