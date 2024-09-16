import axios from 'axios';
import { User } from 'app/schema/types';

const AUTH_TOKEN_KEY = 'auth_token';

export async function login(username: string, password: string): Promise<User> {
  try {
    const response = await axios.post('/api/login', { username, password });
    const { token, user } = response.data;
    localStorage.setItem(AUTH_TOKEN_KEY, token);
    return user;
  } catch (error) {
    // HUMAN ASSISTANCE NEEDED
    // Error handling could be improved based on specific API response structure
    console.error('Login failed:', error);
    throw error;
  }
}

export async function logout(): Promise<void> {
  try {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    await axios.post('/api/logout');
    // Clear any user-related data from the application state
    // This step might require integration with a state management solution like Redux
    // HUMAN ASSISTANCE NEEDED
    // Implement clearing of user-related data from application state
  } catch (error) {
    console.error('Logout failed:', error);
    // Even if the logout request fails, we still remove the token and clear local state
  }
}

export async function getCurrentUser(): Promise<User | null> {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  if (!token) {
    return null;
  }

  try {
    const response = await axios.get('/api/user', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch current user:', error);
    return null;
  }
}

export function isAuthenticated(): boolean {
  return !!localStorage.getItem(AUTH_TOKEN_KEY);
}