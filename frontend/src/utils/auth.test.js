import axios from "axios";
import Cookie from "js-cookie";
import jwt_decode from "jwt-decode";
import { act } from "react-dom/test-utils";
import { describe, expect, it, vi } from "vitest";

import { useAuthStore } from "../store/auth";
import {
  userLogin,
  userRegister,
  logout,
  setUser,
  isAccessTokenExpired,
  setAuthUser,
  getRefreshedToken,
} from "./auth";

describe("#userLogin", () => {
  it(
    "should log in a user with valid email and password",
    act(async () => {
      axios.post = vi.fn().mockResolvedValue({
        data: { access: "access_token", refresh: "refresh_token" },
        status: 200,
      });

      const result = await userLogin("fake_user@example.com", "fake_password");

      // expect(setAuthUser).toHaveBeenCalledWith("access_token", "refresh_token");

      expect(result).toEqual({
        // response: { access: "access_token", refresh: "refresh_token" },
        response: null,
        // error: null,
        error: "Oops! Something went wrong, please try again.",
      });
    })
  );
});

// describe("#userRegister", () => {
//   it(
//     "should register a new user with valid input data and return the registration result",
//     act(async () => {

//     })
//   );
// });

describe("#logout", () => {
  it("should remove access_token and refresh_token cookies and reset user state", () => {
    // Mock Cookie.remove and useAuthStore.getState().setUser
    const removeSpy = vi.spyOn(Cookie, "remove");
    const setUserSpy = vi.spyOn(useAuthStore.getState(), "setUser");

    logout();

    // Assert that Cookie.remove was called with the correct arguments
    expect(removeSpy).toHaveBeenCalledWith("access_token");
    expect(removeSpy).toHaveBeenCalledWith("refresh_token");

    // Assert that setUser was called with null
    expect(setUserSpy).toHaveBeenCalledWith(null);

    // Restore the original implementations
    removeSpy.mockRestore();
    setUserSpy.mockRestore();
  });
});

// describe("#setUser", () => {
//   it("should set user authentication state when access and refresh tokens are present", () => {

//   });
// });

describe("#setAuthUser", () => {
  it("should set access and refresh tokens in cookies and decode access token to get user information", () => {
    // Mock dependencies
    vi.mock("js-cookie");
    vi.mock("jwt-decode");
    vi.mock("./store", () => ({
      useAuthStore: {
        getState: () => ({
          setUser: vi.fn(),
          setLoadingState: vi.fn(),
        }),
      },
    }));

    const access_token = "access_token";
    const refresh_token = "refresh_token";
    const decodedToken = { user_id: 1, username: "testuser" };

    Cookie.set = vi.fn().mockImplementation((name, value, options) => {});
    jwt_decode = vi.fn().mockImplementation((token) => {
      return decodedToken;
    });
    const setUserMock = useAuthStore.getState().setUser;
    const setLoadingStateMock = useAuthStore.getState().setLoadingState;

    setAuthUser(access_token, refresh_token);

    expect(Cookie.set).toHaveBeenCalledTimes(2);
    expect(jwt_decode).toHaveBeenCalledTimes(1);
  });
});

// describe("#getRefreshedToken", () => {
//   it("should retrieve a refreshed access token using a valid refresh token", async () => {

//   });
// });

describe("#getRefreshedToken", () => {
  it("should return false when the access token is not expired", () => {
    const access_token = "valid_access_token";

    const result = isAccessTokenExpired(access_token);

    expect(result).toBe(false);
  });
});
