import React from "react";

function BaseFooter() {
  return (
    <footer className="pt-lg-8 pt-5 footer bg-dark text-white mt-5">
      <div className="container mt-lg-2">
        <div className="row">
          <div className="col-lg-4 col-md-6 col-12 text-white">
            {/* about company */}
            <div className="mb-4">
              <h1>Learning Management System</h1>
              <div className="mt-4">
                <p>
                  The Learning Management System (LMS) is a web application that
                  facilitates online learning, course management, and student
                  engagement.
                </p>
                {/* social media */}
                <div className="fs-4 mt-4">
                  {/*Facebook*/}
                  <a href="#" className="me-2 text-white">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width={16}
                      height={16}
                      fill="currentColor"
                      className="bi bi-facebook"
                      viewBox="0 0 16 16"
                    >
                      <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z" />
                    </svg>
                  </a>
                  {/*Twitter*/}
                  <a href="#" className="me-2 text-white">
                    <svg
                      xmlns="http://www.w3.org/2000/svg "
                      width={16}
                      height={16}
                      fill="currentColor"
                      className="bi bi-twitter"
                      viewBox="0 0 16 16"
                    >
                      <path d="M5.026 15c6.038 0 9.341-5.003 9.341-9.334 0-.14 0-.282-.006-.422A6.685 6.685 0 0 0 16 3.542a6.658 6.658 0 0 1-1.889.518 3.301 3.301 0 0 0 1.447-1.817 6.533 6.533 0 0 1-2.087.793A3.286 3.286 0 0 0 7.875 6.03a9.325 9.325 0 0 1-6.767-3.429 3.289 3.289 0 0 0 1.018 4.382A3.323 3.323 0 0 1 .64 6.575v.045a3.288 3.288 0 0 0 2.632 3.218 3.203 3.203 0 0 1-.865.115 3.23 3.23 0 0 1-.614-.057 3.283 3.283 0 0 0 3.067 2.277A6.588 6.588 0 0 1 .78 13.58a6.32 6.32 0 0 1-.78-.045A9.344 9.344 0 0 0 5.026 15z" />
                    </svg>
                  </a>
                  {/*GitHub*/}
                  <a href="#" className="text-white">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width={16}
                      height={16}
                      fill="currentColor"
                      className="bi bi-github"
                      viewBox="0 0 16 16"
                    >
                      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z" />
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div className="offset-lg-1 col-lg-2 col-md-3 col-6">
            <div className="mb-4">
              {/* list */}
              <h3 className="fw-bold mb-3">Company</h3>
              <ul className="list-unstyled nav nav-footer flex-column nav-x-0">
                <li>
                  <a href="#" className="nav-link text-white">
                    About
                  </a>
                </li>
                <li>
                  <a href="#" className="nav-link text-white">
                    Pricing
                  </a>
                </li>
                <li>
                  <a href="#" className="nav-link text-white">
                    Blog
                  </a>
                </li>
                <li>
                  <a href="#" className="nav-link text-white">
                    Careers
                  </a>
                </li>
                <li>
                  <a href="#" className="nav-link text-white">
                    Contact
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="col-lg-2 col-md-3 col-6">
            <div className="mb-4">
              {/* list */}
              <h3 className="fw-bold mb-3">Support</h3>
              <ul className="list-unstyled nav nav-footer flex-column nav-x-0">
                <li>
                  <a href="#" className="nav-link text-white">
                    Help and Support
                  </a>
                </li>
                <li>
                  <a href="#" className="nav-link text-white">
                    Become Instructor
                  </a>
                </li>
                <li>
                  <a href="#" className="nav-link text-white">
                    Get the app
                  </a>
                </li>
                <li>
                  <a href="#" className="nav-link text-white">
                    FAQ’s
                  </a>
                </li>
                <li>
                  <a href="#" className="nav-link text-white">
                    Tutorial
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="col-lg-3 col-md-12">
            {/* contact info */}
            <div className="mb-4">
              <h3 className="fw-bold mb-3">Get in touch</h3>
              <p>123 Main Street, UK</p>
              <p className="mb-1">
                Email:
                <a href="#" className="text-white">
                  {" "}
                  support@lms.com
                </a>
              </p>
              <p>
                Phone:
                <span className="text-dark fw-semibold">(+44) 123 456 789</span>
              </p>
            </div>
          </div>
        </div>
        <div className="row align-items-center g-0 border-top py-2 mt-6">
          {/* Desc */}
          <div className="col-md-10 col-12">
            <div className="d-lg-flex align-items-center">
              <div className="me-4">
                <span>
                  ©<span id="copyright5"></span>
                  Learning Management System
                </span>
              </div>
              <div>
                <nav className="nav nav-footer">
                  <a className="nav-link text-white ps-0" href="#">
                    Privacy Policy
                  </a>
                  <a className="nav-link text-white px-2 px-md-3" href="#">
                    Cookie Notice
                  </a>
                  <a className="nav-link text-white d-none d-lg-block" href="#">
                    Do Not Sell My Personal Information
                  </a>
                  <a className="nav-link text-white" href="#">
                    Terms of Use
                  </a>
                </nav>
              </div>
            </div>
          </div>
          {/* Links */}
          <div className="col-12 col-md-2 d-md-flex justify-content-end">
            <div className="dropdown">
              <a
                href="#"
                className="dropdown-toggle text-body"
                id="dropdownMenuLink"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <i className="fe fe-globe me-2 align-middle" />
                Language
              </a>
              <ul className="dropdown-menu" aria-labelledby="dropdownMenuLink">
                <li>
                  <a className="dropdown-item" href="#">
                    <span className="me-2">
                      <svg
                        width={16}
                        height={13}
                        viewBox="0 0 16 13"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <g clipPath="url(#clip0_5543_19736)">
                          <path d="M0 0.5H16V12.5H0V0.5Z" fill="#012169" />
                          <path
                            d="M1.875 0.5L7.975 5.025L14.05 0.5H16V2.05L10 6.525L16 10.975V12.5H14L8 8.025L2.025 12.5H0V11L5.975 6.55L0 2.1V0.5H1.875Z"
                            fill="white"
                          />
                          <path
                            d="M10.6 7.525L16 11.5V12.5L9.225 7.525H10.6ZM6 8.025L6.15 8.9L1.35 12.5H0L6 8.025ZM16 0.5V0.575L9.775 5.275L9.825 4.175L14.75 0.5H16ZM0 0.5L5.975 4.9H4.475L0 1.55V0.5Z"
                            fill="#C8102E"
                          />
                          <path
                            d="M6.025 0.5V12.5H10.025V0.5H6.025ZM0 4.5V8.5H16V4.5H0Z"
                            fill="white"
                          />
                          <path
                            d="M0 5.325V7.725H16V5.325H0ZM6.825 0.5V12.5H9.225V0.5H6.825Z"
                            fill="#C8102E"
                          />
                        </g>
                        <defs>
                          <clipPath id="clip0_5543_19736">
                            <rect
                              width={16}
                              height={12}
                              fill="white"
                              transform="translate(0 0.5)"
                            />
                          </clipPath>
                        </defs>
                      </svg>
                    </span>
                    English
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="#">
                    <span className="me-2">
                      <svg
                        width={16}
                        height={13}
                        viewBox="0 0 16 13"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <g clipPath="url(#clip0_5543_19744)">
                          <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M0 0.5H16V12.5H0V0.5Z"
                            fill="white"
                          />
                          <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M0 0.5H5.3325V12.5H0V0.5Z"
                            fill="#002654"
                          />
                          <path
                            fillRule="evenodd"
                            clipRule="evenodd"
                            d="M10.668 0.5H16.0005V12.5H10.668V0.5Z"
                            fill="#CE1126"
                          />
                        </g>
                        <defs>
                          <clipPath id="clip0_5543_19744">
                            <rect
                              width={16}
                              height={12}
                              fill="white"
                              transform="translate(0 0.5)"
                            />
                          </clipPath>
                        </defs>
                      </svg>
                    </span>
                    Français
                  </a>
                </li>
                <li>
                  <a className="dropdown-item" href="#">
                    <span className="me-2">
                      <svg
                        width={16}
                        height={13}
                        viewBox="0 0 16 13"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <g clipPath="url(#clip0_5543_19751)">
                          <path d="M0 8.5H16V12.5H0V8.5Z" fill="#FFCE00" />
                          <path d="M0 0.5H16V4.5H0V0.5Z" fill="black" />
                          <path d="M0 4.5H16V8.5H0V4.5Z" fill="#DD0000" />
                        </g>
                        <defs>
                          <clipPath id="clip0_5543_19751">
                            <rect
                              width={16}
                              height={12}
                              fill="white"
                              transform="translate(0 0.5)"
                            />
                          </clipPath>
                        </defs>
                      </svg>
                    </span>
                    Deutsch
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default BaseFooter;
