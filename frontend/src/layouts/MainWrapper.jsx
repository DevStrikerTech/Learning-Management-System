import { useEffect, useState } from "react";

import { setUser } from "../utils/auth";

/**
 * Custom hook to wrap components with a loading state.
 * @param {Object} props - The component props.
 * @param {ReactNode} props.children - The child components to render.
 * @returns {ReactNode} The wrapped components.
 */
const MainWrapper = ({ children }) => {
  const [loadingState, setLoadingState] = useState(true);

  useEffect(() => {
    const handler = async () => {
      setLoadingState(true);

      await setUser();

      setLoadingState(false);
    };

    handler();
  }, []);

  return <>{loadingState ? null : children}</>;
};

export default MainWrapper;
