import axios from "axios";
import Cookies from "js-cookie";
import { act } from "react-dom/test-utils";
import { describe, expect, it, vi } from "vitest";

describe("#useAxios", () => {
  it(
    "should return an Axios instance with the correct base URL and authorization header when access token is present in cookies",
    act(async () => {
      Cookies.get = vi.fn().mockReturnValue("access_token");

      axios.create = vi.fn().mockReturnValue({
        interceptors: {
          request: {
            use: vi.fn(),
          },
        },
      });

      // Dynamically import the useAxios function
      const { default: useAxios } = await import("./useAxios");

      const axiosInstance = useAxios();

      expect(axios.create).toHaveBeenCalledWith({
        baseURL: "http://127.0.0.1:8000/api/v1/",
        headers: { Authorization: "Bearer access_token" },
      });
    })
  );
});
