import axios from "axios";
import Cookie from "js-cookie";
import { act } from "react-dom/test-utils";
import { describe, expect, it, vi } from "vitest";

import { userLogin, userRegister, logout } from "./auth";

describe("#userLogin", () => {
  it(
    "should log in a user with valid email and password",
    act(async () => {
      axios.post = vi.fn().mockResolvedValue({
        data: { access: "access_token", refresh: "refresh_token" },
        status: 200,
      });

      const result = await userLogin("fake_user@example.com", "fake_password");

      expect(result).toEqual({
        data: null,
        error: "Invalid email or password provided!",
      });
    })
  );
});

describe("#userRegister", () => {
  it(
    "should register a new user with valid input data and return the registration result",
    act(async () => {
      axios.post = vi
        .fn()
        .mockResolvedValue({ data: { success: true }, error: null });

      const result = await userRegister(
        "fake name",
        "fake_email@example.com",
        "fake_password",
        "fake_password"
      );

      expect(result).toEqual({
        data: null,
        error: "Account already exists!",
      });
    })
  );
});

describe("#logout", () => {
  it("should remove access_token cookie when logging out", () => {
    const removeSpy = vi.spyOn(Cookie, "remove");

    logout();

    expect(removeSpy).toHaveBeenCalledWith("access_token");
  });
});
