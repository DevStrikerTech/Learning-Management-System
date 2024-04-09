import React from "react";
import { act } from "react-dom/test-utils";
import { describe, it, expect, vi } from "vitest";
import { render, waitFor } from "@testing-library/react";

import MainWrapper from "../layouts/MainWrapper";

// Mock the setUser function to return undefined
vi.mock("../utils/auth", () => ({
  setUser: vi.fn().mockResolvedValue(undefined),
}));

describe("#MainWrapper", () => {
  it(
    "should render children when loading is complete",
    act(async () => {
      // Render MainWrapper component
      const { container } = render(
        <MainWrapper>
          <div>Child Component</div>
        </MainWrapper>
      );

      // Wait for the child component to be rendered
      await waitFor(() => {
        expect(container.textContent).toContain("Child Component");
      });
    })
  );
});
