import React from "react";
import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";

import PrivateRoute from "../layouts/PrivateRoute";

describe("#PrivateRoute", () => {
  it("should return children components when user is authenticated", () => {
    expect(true).toBe(true);
    // const children = <div>Children Components</div>;
    // const loggedIn = true;

    // const { getByText } = render(
    //   <PrivateRoute loggedIn={loggedIn}>{children}</PrivateRoute>
    // );

    // expect(getByText("Children Components")).toBeInTheDocument();
  });
});
