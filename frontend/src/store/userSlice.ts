import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import { User } from '../schema/types';
import { auth } from '../services/auth';

// HUMAN ASSISTANCE NEEDED
// The login function has a confidence level of 0.7, which is below the threshold of 0.8.
// Please review and adjust the implementation as needed.
export const login = createAsyncThunk<User, { username: string, password: string }>(
  'user/login',
  async ({ username, password }, { rejectWithValue }) => {
    try {
      const user = await auth.login(username, password);
      return user;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: {
    currentUser: null as User | null,
    status: 'idle',
    error: null as string | null,
  },
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.currentUser = action.payload;
    },
    clearUser: (state) => {
      state.currentUser = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.currentUser = action.payload;
        state.error = null;
      })
      .addCase(login.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload as string;
      });
  },
});

export const { setUser, clearUser } = userSlice.actions;
export default userSlice.reducer;