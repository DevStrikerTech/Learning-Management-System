import { describe, it, expect } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { render, screen } from "@testing-library/react";

import App from "./App";
import { CartContext, ProfileContext } from "./views/plugin/Context";

describe("#App", () => {
  it("renders without crashing and displays auth routes", async () => {
    const cartValue = [0, () => {}]; // Mock cart state
    const profileValue = [{}, () => {}]; // Mock profile state

    render(
      <MemoryRouter initialEntries={["/register/"]}>
        <CartContext.Provider value={cartValue}>
          <ProfileContext.Provider value={profileValue}>
            <App />
          </ProfileContext.Provider>
        </CartContext.Provider>
      </MemoryRouter>
    );

    // Assertions to verify the rendering of routes and components
    expect(await screen.findByText(/register/i)).toBeInTheDocument();
    expect(await screen.findByText(/login/i)).toBeInTheDocument();
  });
});
