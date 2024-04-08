import { Navigate } from "react-router-dom";

import { useAuthStore } from "../store/auth";

/**
 * A higher-order component that wraps around protected routes to enforce authentication.
 * If the user is not logged in, it redirects to the login page.
 *
 * @param {Object} props - The component props.
 * @param {ReactNode} props.children - The components that are children of this route.
 * @returns {ReactNode} Either the children components if the user is authenticated, or a redirection to the login page.
 */
const PrivateRoute = ({ children }) => {
  const loggedIn = useAuthStore((state) => state.isLoggedIn)();

  return loggedIn ? <>{children}</> : <Navigate to="/login/" />;
};

export default PrivateRoute;
