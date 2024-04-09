import axios from "./axios";
import Cookie from "js-cookie";
import jwt_decode from "jwt-decode";

import { useAuthStore } from "../store/auth";

/**
 * Attempts to log in a user with the provided credentials.
 *
 * @param {string} email - The user's email address.
 * @param {string} password - The user's password.
 * @returns {Promise<{ response: Object | null, error: string | null }>}
 * An object containing the login response data or an error message.
 */
export const userLogin = async (email, password) => {
  // Define a mapping of field names to their display names
  const fieldDisplayNames = {
    email: "Email Address",
    password: "Password",
  };

  try {
    const { data, status } = await axios.post(`user/token/`, {
      email,
      password,
    });

    if (status === 200) {
      setAuthUser(data.access, data.refresh);
      return { response: data, error: null };
    }
  } catch (error) {
    let errorMessages = [];

    // Handle non-200 status within the catch block
    if (error.response) {
      if (error.response.status !== 200 && error.response.data?.detail) {
        return { response: null, error: error.response.data.detail };
      }

      if (typeof error.response.data === "object") {
        for (const [field, messages] of Object.entries(error.response.data)) {
          if (Array.isArray(messages)) {
            const displayName = fieldDisplayNames[field] || field;
            errorMessages.push(
              ...messages.map((message) => `${displayName}: ${message}`)
            );
          }
        }
      }
    }

    const errorResponse =
      errorMessages.length > 0
        ? errorMessages.join("\n")
        : "Oops! Something went wrong, please try again.";

    return { response: null, error: errorResponse };
  }
};

/**
 * Asynchronously registers a new user with the provided credentials.
 *
 * @param {Object} params - The user registration parameters.
 * @param {string} params.fullName - The full name of the user.
 * @param {string} params.email - The email address of the user.
 * @param {string} params.password - The password for the user's account.
 * @param {string} params.confirmPassword - The confirmation of the user's password, must match the password.
 * @returns {Promise<Object>} A promise that resolves to an object containing either the registration response data or an error message.
 * @throws {Error} Throws an error if the registration process fails at any point.
 */
export const userRegister = async (
  full_name,
  email,
  password,
  password_matched
) => {
  // Define a mapping of field names to their replacements
  const fieldReplacements = {
    full_name: "Full Name",
    email: "Email Address",
    password: "Password",
    password_matched: "Confirm Password",
  };

  try {
    const { data } = await axios.post(`user/register/`, {
      full_name,
      email,
      password,
      password_matched,
    });

    await userLogin(email, password);
    return { data, error: null };
  } catch (error) {
    let errorMessages = [];

    if (error.response && Array.isArray(error.response.data)) {
      errorMessages = error.response.data.map(
        (message, index) => `Error ${index + 1}: ${message}`
      );
    } else if (error.response && typeof error.response.data === "object") {
      for (const [field, messages] of Object.entries(error.response.data)) {
        if (Array.isArray(messages)) {
          const displayName = fieldReplacements[field] || field;
          errorMessages.push(
            ...messages.map((message) => `${displayName}: ${message}`)
          );
        }
      }
    }

    const errorResponse =
      errorMessages.length > 0
        ? errorMessages.join("\n")
        : "Oops! Something went wrong, please try again.";

    return {
      data: null,
      error: errorResponse,
    };
  }
};

/**
 * Logs out the user by removing access and refresh tokens from cookies and resetting the user state.
 */
export const logout = () => {
  Cookie.remove("access_token");
  Cookie.remove("refresh_token");
  useAuthStore.getState().setUser(null);
};

/**
 * Sets the user authentication state based on access and refresh tokens stored in cookies.
 * If the access token is expired, it attempts to refresh it using the refresh token.
 * Otherwise, it sets the user with the existing tokens.
 */
export const setUser = async () => {
  const access_token = Cookie.get("access_token");
  const refresh_token = Cookie.get("refresh_token");

  if (!access_token || !refresh_token) {
    return;
  }

  if (isAccessTokenExpired(access_token)) {
    const response = getRefreshedToken(refresh_token);
    setAuthUser(response.access, response.refresh);
  } else {
    setAuthUser(access_token, refresh_token);
  }
};

/**
 * Sets the user authentication state based on access and refresh tokens stored in cookies.
 * If the access token is expired, it attempts to refresh it using the refresh token.
 * Otherwise, it sets the user with the existing tokens.
 */
export const setAuthUser = async (access_token, refresh_token) => {
  Cookie.set("access_token", access_token, {
    expires: 1,
    secure: true,
  });

  Cookie.set("refresh_token", refresh_token, {
    expires: 7,
    secure: true,
  });

  const user = jwt_decode(access_token) ?? null;

  if (user) {
    useAuthStore.getState().setUser(user);
  }
  useAuthStore.getState().setLoadingState(false);
};

/**
 * Retrieves a refreshed access token using the provided refresh token.
 *
 * @returns {Promise<{ access: string, refresh: string }>} - The refreshed tokens.
 */
export const getRefreshedToken = async () => {
  const refresh_token = Cookie.get("refresh_token");
  const response = await axios.post(`user/token/refresh/`, {
    refresh: refresh_token,
  });
  return response.data;
};

/**
 * Checks if the provided access token is expired.
 *
 * @param {string} access_token - The access token to check.
 * @returns {boolean} - `true` if the token is expired, otherwise `false`.
 */
export const isAccessTokenExpired = (access_token) => {
  try {
    const decodedToken = jwt_decode(access_token);
    return decodedToken.exp < Date.now() / 1000;
  } catch (error) {
    return true;
  }
};
