[![atl-text-8](https://img.shields.io/badge/Version-4.2.7-blueviolet?logo=Django&style=flat)](https://www.djangoproject.com/) [![atl-text-1](https://img.shields.io/badge/Version-18-blue?logo=React&style=flat)](https://react.dev/) [![atl-text-2](https://img.shields.io/badge/Version-3.10-red?logo=Python&style=flat)](https://www.python.org/) ![atl-text-6](https://img.shields.io/badge/license-GPL-lightgrey) ![atl-text-7](https://img.shields.io/badge/coverage-83-green) [![LMS Build](https://github.com/DevStrikerTech/Learning-Management-System/actions/workflows/backend_build.yml/badge.svg)](https://github.com/DevStrikerTech/Learning-Management-System/actions/workflows/backend_build.yml)

# Learning Management System (LMS)

The Learning Management System (LMS) is a web application that facilitates online learning, managing courses, and student engagement. It combines the power of **Django** for backend development and **React.js** for frontend user interfaces.

## Features

- **User Authentication and Authorization**: Secure user login and role-based access control.
- **Course Creation and Enrollment**: Instructors can create courses, and students can enroll in them.
- **Content Delivery**: Upload and organize course materials such as videos, documents, and quizzes.
- **Progress Tracking and Analytics**: Monitor student progress, completion rates, and performance.
- **Discussion Forums**: Enable communication and collaboration among students and instructors.
- **User Profiles**: Personalized profiles for learners and educators.

## Technologies Used

<p align="left">
   <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a>
    <a href="https://reactjs.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original-wordmark.svg" alt="react" width="40" height="40"/> </a>
   <a href="https://redux.js.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/redux/redux-original.svg" alt="redux" width="40" height="40"/> 
   </a> <a href="https://sass-lang.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/sass/sass-original.svg" alt="sass" width="40" height="40"/> </a>
   <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> 
</p>


- **Django**: A high-level Python web framework for backend development.
- **React.js**: A JavaScript library for building interactive user interfaces.
- **React Router**: For client-side routing.
- **Redux**: For state management.
- **SASS**: Used for styling components.
- **Vite**: Bundles frontend assets.
- **PostgreSQL**: Powerful relational database management system.

## Getting Started

1. **Clone the Repository**:

   ```
   git clone https://github.com/DevStrikerTech/Learning-Management-System.git
   ```

2. **Backend Setup**:

- Navigate to the `backend` directory.
- Install dependencies:

  ```
  pip install poetry
  poetry install
  ```

- Set up the database:
  ```
  poetry run python manage.py migrate
  ```
- Run the development server:
  ```
  poetry run python manage.py runserver
  ```
  Run the tests:
  ```
  poetry run coverage run manage.py test
  poetry run coverage report
  ```

3. **Frontend Setup**:

- Navigate to the `frontend` directory.
- Install dependencies:
  ```
  yarn install
  ```
- Start the frontend application locally:
  ```
  yarn dev
  ```

4. **Access the Application**:

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Development Flow

1. Create a new feature branch:
   git checkout -b feature/<issue-number>-<short-description>

2. Develop the feature, committing atomic changes.

3. Ensure tests pass:

   ```
   yarn run test
   ```

4. Create a Pull Request and get feedback.

5. After approval, merge into the `develop` branch.

## Contributing

Contributions are more than welcome! Please follow the guidelines in CONTRIBUTING.md.

## License

This project is licensed under the GPL-3.0 License. See [LICENSE](LICENSE) for details.
