import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import { Tweet } from '../schema/types';
import api from '../services/api';

// HUMAN ASSISTANCE NEEDED
// The fetchTweets function has a confidence level of 0.7, which is below the threshold of 0.8.
// Please review and adjust the implementation as needed.
export const fetchTweets = createAsyncThunk<Tweet[], { page: number, limit: number }>(
  'tweets/fetchTweets',
  async ({ page, limit }) => {
    try {
      const response = await api.get(`/tweets?page=${page}&limit=${limit}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
);

const tweetSlice = createSlice({
  name: 'tweets',
  initialState: {
    tweets: [] as Tweet[],
    status: 'idle',
    error: null as string | null,
  },
  reducers: {
    addTweet: (state, action: PayloadAction<Tweet>) => {
      state.tweets.unshift(action.payload);
    },
    updateTweet: (state, action: PayloadAction<Tweet>) => {
      const index = state.tweets.findIndex(tweet => tweet.id === action.payload.id);
      if (index !== -1) {
        state.tweets[index] = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTweets.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchTweets.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.tweets = action.payload;
      })
      .addCase(fetchTweets.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message || 'An error occurred';
      });
  },
});

export const { addTweet, updateTweet } = tweetSlice.actions;
export default tweetSlice.reducer;