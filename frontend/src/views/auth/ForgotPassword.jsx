import { useState } from "react";
import Toast from "../plugin/Toast";

import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";

import apiInstance from "../../utils/axios";

function ForgotPassword() {
  const [userEmail, setUserEmail] = useState("");
  const [isLoadingState, setIsLoadingState] = useState(false);

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setIsLoadingState(true);
    try {
      await apiInstance.get(`user/password-reset/${userEmail}/`).then((res) => {
        setIsLoadingState(false);
        Toast().fire({
          icon: "success",
          title: "Password Reset Email Sent",
        });
      });
    } catch (error) {
      // console.log("error: ", error);
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
                  <h1 className="mb-1 fw-bold">Forgot Password</h1>
                  <span>Let's help you get back into your account</span>
                </div>
                <form
                  className="needs-validation"
                  noValidate=""
                  onSubmit={handleForgotPassword}
                >
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
                      required
                      onChange={(e) => setUserEmail(e.target.value)}
                    />
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
                          Reset Password <i className="fas fa-arrow-right"></i>
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

export default ForgotPassword;
