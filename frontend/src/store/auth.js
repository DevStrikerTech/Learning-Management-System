import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";

/**
 * Creates an instance of the authentication store.
 * @param {function} setAuthStore - Setter function provided by Zustand.
 * @param {function} getAuthStore - Getter function provided by Zustand.
 * @returns {Object} The authentication store object.
 */
const useAuthStore = create((setAuthStore, getAuthStore) => ({
  allUserData: null,
  loadingState: false,

  /**
   * Retrieves user data.
   * @returns {{user_id: string|null, username: string|null}} User data.
   */
  getUser: () => ({
    user_id: getAuthStore().allUserData?.user_id || null,
    username: getAuthStore().allUserData?.username || null,
  }),

  /**
   * Sets user data.
   * @param {{user_id: string|null, username: string|null}} getUser - User data to set.
   */
  setUser: (getUser) => ({
    allUserData: getUser,
  }),

  /**
   * Updates the loading state.
   * @param {boolean} loadingState - New loading state value.
   */
  setLoadingState: (loadingState) => setAuthStore({ loadingState }),

  /**
   * Checks if the user is logged in.
   * @returns {boolean} True if the user is logged in, false otherwise.
   */
  isLoggedIn: () => getAuthStore().allUserData !== null,
}));

// Enable store devtools in development mode
if (import.meta.env.DEV) {
  mountStoreDevtool("Store", useAuthStore);
}

export { useAuthStore };
