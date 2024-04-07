import axios from "axios";
import Cookies from "js-cookie";

import { API_BASE_URL } from "./constants";
import { getRefreshedToken, isAccessTokenExpired, setAuthUser } from "./auth";

/**
 * Custom hook to create an Axios instance with authentication headers.
 * @returns {AxiosInstance} The configured Axios instance.
 */
const useAxios = () => {
  const accessToken = Cookies.get("access_token");
  const refreshToken = Cookies.get("refresh_token");

  const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: { Authorization: `Bearer ${accessToken}` },
  });

  axiosInstance.interceptors.request.use(async (req) => {
    if (!isAccessTokenExpired) {
      return req;
    }

    const response = await getRefreshedToken(refreshToken);

    setAuthUser(response.access, response.refresh);
    req.headers.Authorization = `Bearer ${response.data?.access}`;

    return req;
  });

  return axiosInstance;
};

export default useAxios;
