import { describe, it, expect } from "vitest";
import { CartContext, ProfileContext } from "./Context";

describe("#Context", () => {
  it("should create CartContext", () => {
    expect(CartContext).toBeDefined();
    expect(typeof CartContext.Provider).toBe("object");
    expect(typeof CartContext.Consumer).toBe("object");
  });

  it("should create ProfileContext", () => {
    expect(ProfileContext).toBeDefined();
    expect(typeof ProfileContext.Provider).toBe("object");
    expect(typeof ProfileContext.Consumer).toBe("object");
  });
});
