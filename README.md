[![atl-text-8](https://img.shields.io/badge/Version-4.2.7-blueviolet?logo=Django&style=flat)](https://www.djangoproject.com/) [![atl-text-1](https://img.shields.io/badge/Version-18-blue?logo=React&style=flat)](https://react.dev/) [![atl-text-2](https://img.shields.io/badge/Version-3.10.12-red?logo=Python&style=flat)](https://www.python.org/) ![atl-text-6](https://img.shields.io/badge/license-GPL-lightgrey) ![atl-text-7](https://img.shields.io/badge/coverage-94-green) [![LMS Build](https://github.com/DevStrikerTech/Learning-Management-System/actions/workflows/build.yml/badge.svg)](https://github.com/DevStrikerTech/Learning-Management-System/actions/workflows/build.yml)

# Learning Management System (LMS)

The Learning Management System (LMS) is a web application that facilitates online learning, course management, and student engagement. It combines the power of **Django** for backend development and **React.js** for frontend user interfaces.

## Features

- **User Authentication and Authorization**: Secure user login and role-based access control.
- **Course Creation and Enrollment**: Instructors can create courses, and students can enroll in them.
- **Content Delivery**: Upload and organize course materials such as videos, documents, and quizzes.
- **Progress Tracking and Analytics**: Monitor student progress, completion rates, and performance.
- **Discussion Forums**: Enable communication and collaboration among students and instructors.
- **User Profiles**: Personalized profiles for learners and educators.

## Technologies Used

- **Django**: A high-level Python web framework for backend development.
- **React.js**: A JavaScript library for building interactive user interfaces.
- **React Router**: For client-side routing.
- **Redux**: For state management.
- **SASS**: Used for styling components.
- **Webpack**: Bundles frontend assets.
- **PostgreSQL**: As the database.

## Getting Started

1. **Clone the Repository**:

```
git clone https://github.com/DevStrikerTech/Learning-Management-System.git
```

2. **Backend Setup**:

- Navigate to the `backend` directory.
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```
- Set up the database:
  ```
  python manage.py migrate
  ```
- Run the development server:
  ```
  python manage.py runserver
  ```

3. **Frontend Setup**:

- Navigate to the `frontend` directory.
- Install dependencies:
  ```
  npm install
  ```
- Start the frontend application locally:
  ```
  npm start
  ```

4. **Access the Application**:

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Development Flow

1. Create a new feature branch:
   git checkout -b feature/<issue-number>-<short-description>

2. Develop the feature, committing atomic changes.

3. Ensure tests pass:

```
npm test
```

4. Create a Pull Request and get feedback.

5. After approval, merge into the `develop` branch.

## Contributing

Contributions are welcome! Please follow the guidelines in CONTRIBUTING.md.

## License

This project is licensed under the GPL-3.0 License. See LICENSE for details.
