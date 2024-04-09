import { describe, it, expect } from "vitest";
import Toast from "./Toast";

describe("#Toast", () => {
  it("should return a Swal object configured as a toast notification", () => {
    const toast = Toast();

    expect(toast.toast).toBe(undefined);
    expect(toast.position).toBe(undefined);
    expect(toast.showConfirmButton).toBe(undefined);
    expect(toast.timer).toBe(undefined);
    expect(toast.timerProgressBar).toBe(undefined);
  });
});
