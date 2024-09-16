import { configureStore } from '@reduxjs/toolkit';
import { tweetReducer } from './tweetSlice';
import { userReducer } from './userSlice';

const setupStore = () => {
  return configureStore({
    reducer: {
      tweets: tweetReducer,
      user: userReducer,
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware(),
    devTools: process.env.NODE_ENV !== 'production',
  });
};

export const store = setupStore();

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;