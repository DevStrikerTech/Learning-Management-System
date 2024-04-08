import { useState } from "react";
import Toast from "../plugin/Toast";
import { Link, useNavigate } from "react-router-dom";

import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";

import { userLogin } from "../../utils/auth";

function Login() {
  const [userEmail, setUserEmail] = useState("");
  const [userPassword, setUserPassword] = useState("");
  const [isLoadingState, setIsLoadingState] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoadingState(true);
    const { error } = await userLogin(userEmail, userPassword);
    if (error) {
      setIsLoadingState(false);
      Toast().fire({
        icon: "warning",
        text: error,
      });
    } else {
      navigate("/");
      setIsLoadingState(false);
    }
  };

  return (
    <>
      <BaseHeader />

      <section
        className="container d-flex flex-column vh-100"
        style={{ marginTop: "150px" }}
      >
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Sign in</h1>
                  <span>
                    Don’t have an account?
                    <Link to="/register/" className="ms-1">
                      Sign up
                    </Link>
                  </span>
                </div>
                {/* Form */}
                <form
                  className="needs-validation"
                  noValidate=""
                  onSubmit={handleLogin}
                >
                  {/* Username */}
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                      Email Address
                    </label>
                    <input
                      type="email"
                      id="email"
                      className="form-control"
                      name="email"
                      placeholder="johndoe@gmail.com"
                      required=""
                      onChange={(e) => setUserEmail(e.target.value)}
                    />
                    <div className="invalid-feedback">
                      Please enter valid username.
                    </div>
                  </div>
                  {/* Password */}
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e) => setUserPassword(e.target.value)}
                    />
                    <div className="invalid-feedback">
                      Please enter valid password.
                    </div>
                  </div>
                  {/* Checkbox */}
                  <div className="d-lg-flex justify-content-between align-items-center mb-4">
                    <div className="form-check">
                      <input
                        type="checkbox"
                        className="form-check-input"
                        id="rememberme"
                        required=""
                      />
                      <label className="form-check-label" htmlFor="rememberme">
                        Remember me
                      </label>
                      <div className="invalid-feedback">
                        You must agree before submitting.
                      </div>
                    </div>
                    <div>
                      <Link to="/forgot-password/">Forgot your password?</Link>
                    </div>
                  </div>
                  <div>
                    <div className="d-grid">
                      {isLoadingState === true && (
                        <button
                          disabled
                          type="submit"
                          className="btn btn-danger"
                        >
                          Processing <i className="fas fa-spinner fa-spin"></i>
                        </button>
                      )}

                      {isLoadingState === false && (
                        <button type="submit" className="btn btn-danger">
                          Sign in <i className="fas fa-sign-in-alt"></i>
                        </button>
                      )}
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  );
}

export default Login;
