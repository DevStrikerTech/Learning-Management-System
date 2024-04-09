import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";

describe("#main", () => {
  it("renders without crashing", () => {
    // Create a new div element to serve as the root for your React app
    const root = document.createElement("div");
    root.id = "root";
    document.body.appendChild(root);

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
      root
    );

    // expect(screen.getByText(/index page is not ready yet/i)).toBeInTheDocument();

    // Clean up by removing the appended root element after the test
    document.body.removeChild(root);
  });
});
