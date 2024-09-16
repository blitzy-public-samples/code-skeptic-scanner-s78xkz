// Utility functions for input validation

/**
 * Validates an email address
 * @param email - The email address to validate
 * @returns True if email is valid, false otherwise
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// HUMAN ASSISTANCE NEEDED
/**
 * Validates a password against specified criteria
 * @param password - The password to validate
 * @returns True if password meets criteria, false otherwise
 */
export const isValidPassword = (password: string): boolean => {
  // Minimum length requirement (e.g., 8 characters)
  const minLength = 8;
  
  // Regular expressions for different criteria
  const uppercaseRegex = /[A-Z]/;
  const lowercaseRegex = /[a-z]/;
  const numberRegex = /[0-9]/;
  const specialCharRegex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;

  // Check all criteria
  return (
    password.length >= minLength &&
    uppercaseRegex.test(password) &&
    lowercaseRegex.test(password) &&
    numberRegex.test(password) &&
    specialCharRegex.test(password)
  );
};
// Note: The specific criteria for password validation may need to be adjusted based on project requirements.

/**
 * Validates tweet content length
 * @param content - The tweet content to validate
 * @returns True if content is within valid length, false otherwise
 */
export const isValidTweetContent = (content: string): boolean => {
  const maxTweetLength = 280; // Twitter's current character limit
  return content.length <= maxTweetLength;
};