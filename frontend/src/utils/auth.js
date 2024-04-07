import axios from "./axios";
import Cookie from "js-cookie";
import jwt_decode from "jwt-decode";

import { useAuthStore } from "../store/auth";

/**
 * Logs in a user with the provided email and password.
 *
 * @param {string} userEmail - The user's email address.
 * @param {string} userPassword - The user's password.
 * @returns {Promise<{ data: any, error: string | null }>} - The login result.
 */
export const userLogin = async (userEmail, userPassword) => {
  try {
    const { data, status } = await axios.post(`user/token/`, {
      userEmail,
      userPassword,
    });

    if (status === 200) {
      setAuthUser(data.access, data.refresh);
    }

    return { data, error: null };
  } catch (error) {
    return {
      data: null,
      error: "Invalid email or password provided!",
    };
  }
};

/**
 * Registers a user with the provided information.
 *
 * @param {string} userFullName - The user's full name.
 * @param {string} userEmail - The user's email address.
 * @param {string} userPassword - The user's password.
 * @param {string} userPasswordMatched - The confirmation of the user's password.
 * @returns {Promise<{ data: any, error: string | null }>} - The registration result.
 */
export const userRegister = async (
  userFullName,
  userEmail,
  userPassword,
  userPasswordMatched
) => {
  try {
    const { data } = await axios.post(`user/register/`, {
      userFullName,
      userEmail,
      userPassword,
      userPasswordMatched,
    });

    await login(userEmail, userPassword);
    return { data, error: null };
  } catch (error) {
    return {
      data: null,
      error: "Account already exists!",
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
